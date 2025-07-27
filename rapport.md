## Introduction
Ce rapport présente une analyse des risques détectés sur le lieu de travail à partir de données multi-modales (images, détections, météo, réglementation).

Ce fichier représente un rapport qui met en évidence les différentes étapes pour exécuter le code, apporte des explications, présente les défis rencontrés, les améliorations possibles ainsi que quelques résultats sur les cas de test.

**NOTE: Le code fonctionnera en supposant que les différentes étapes présentes dans <span style="color:orange">train.ipynb</span> ont déjà été effectuées au préalable.**

## Données utilisées
- Images panoramiques HD
- Détections de personnes : Uniquement les personnes avec un score de confiance supérieur à 0,5 <span style="color:orange">**images_EST-1.json & images_EST-2.json**)</span> .
- Météo: <span style="color:orange">**weather_info.json** {forecast,  airquality.forcast}</span> 

## Structure du code
```
enlaps_test/
├── src/
    ├── agents/
    │   ├── report_agent.py
    │   ├── vision_agent.py
    │   └── weather_agent.py
    ├── utils/
    │   ├── config.py
    │   └── risk_management.py
    │   └── util.py
    │   .env    <-- not committed to git (gitignored)
    │   main.py
    └── train.ipynb
├── Dockerfile
├── rapport.md
├── README.md
├── requirements.txt
└── assets/      <-- not committed to git (gitignored)

```

## Agents
-  **vision_agent** : Responsable de l’entraînement et de l’ajustement d’un LLM prenant en entrée un dossier d’images, un fichier JSON décrivant ces images, et générant un fichier XML avec des résultats personnalisés basés sur un prompt.

-  **weather_agent** : Agent simple qui prend en entrée une liste de valeurs météorologiques (par exemple, la température) et retourne un fichier JSON indiquant les risques détectés (par exemple, température > 38 degrés)

- **report_agent** : Prend en entrée les résultats issus des modules météo et vision, et génère un rapport avec des recommandations de sécurité.

- **config.py** : Paramètres d’entraînement et de test tels que les prompts, la température du LLM, ...

- **risk_management** : Contient une fonction qui compare une valeur météorologique à son seuil de risque.

- **util** : Diverses fonctions pour analyser les réponses XML, découper les images, ...


**Note** : Dans vision_agent.py, j’ai créé une fonction qui simule l’étape de test, mais au lieu de prendre un dossier d’images, elle prend un fichier JSON décrivant les résultats des LLMs. La raison derrière cela est de réduire l’utilisation de l’API d’OpenAI.


## How it works
### Vision Agent :
-   Pour chaque image dans le dossier d’entrée, et pour chaque personne détectée dans cette image.

- Prendre le bounding box de la personne, découper l’image selon cette box.

- Générer un prompt demandant à un LLM d’analyser l’image pour vérifier la présence d’une personne et si elle porte des équipements de protection individuelle (PPE).

- Retourner les résultats au format XML.

- Convertir le XML en JSON (1)

### Weather Agent :
- Prendre une série temporelle **(timestamps)** de différentes variables météorologiques et leurs valeurs, et retourner un objet JSON (2) avec chaque timestamps et les risques météorologiques correspondants. 

### Report Agente :
- Prendre un rapport de vision (1) et un rapport météo (2) et générer un rapport détaillé pour chaque image / timestamps ainsi que les risques correspondants en format XML.


## Utilisation

### Lancer en local
```bash
python src/main.py
```

### Construire et lancer avec Docker
```bash
docker build -t risk-analyzer .
docker run --rm risk-analyzer
```

## Détails des résultats
En tenant compte que **images_EST_GT_train.json** et/ou **image_predictions_test.json** ont été générés, l’exécution de main.py produira <span style="color:orange">**report.xml**</span> et <span style="color:orange">**evaluation.txt**</span> :

### report.xml

```

<incidents>
    <incident>
        <timestamp>2025-07-11T13:00</timestamp>
        <image_path>670484413_30a9e6a7-1a81-4f83-89d2-d14f5093f4e1.jpg</image_path>
        <ppe_risks>
            <risk>No PP Equipment</risk>
        </ppe_risks>
        <weather_risks>
            <risk>shortwave_radiation</risk>
        </weather_risks>
        <recommendation>Ensure all workers are wearing the required Personal Protective Equipment (PPE). Limit exposure to shortwave radiation by seeking shade and using sun protection.</recommendation>
    </incident>
    ...
    </incidents>
```


Pour evaluaer **report_agent.py**, je génère une liste d’images présentant des situations à risque (personnes sans PPE) qui se superposent aux risques météorologiques en fonction de leurs timestamps, selon les horaires.
Cette liste est ensuite etait donnée à report_agent pour évaluer les résultats du rapport généré par **report_agent.py** (fichier XML des incidents).

```
{'2025-07-11T13': {
    'image_paths': ['670484413_30a9e6a7-1a81-4f83-89d2-d14f5093f4e1.jpg'], 
    'ppe_risks': [{'No PP Equipment': 1}], 
    'weather_risks': ['shortwave_radiation']}, 
...
```

### evaluation.txt
```
- Accuracy: Both reports accurately identify the same incidents and risks. However, the manual report provides more detailed information about the number of times a risk was identified, which is missing in the AI report. 

...

- Relevance of recommendations: Both reports provide the same recommendations, which are relevant to the identified risks. However, the AI report presents the recommendations in a more clear and concise manner.
```

## Conclusion, Défis et Améliorations
### Conclusion
- Pour les LLMs, le retour des résultats au format XML a été recommandé par OpenAI et plusieurs articles, contrairement au JSON, notament à cause des difficultées d'analyzer les quotation **(")**

- Le XML peut être facilement converti en CSV, JSON, etc.
### Défis
- La clé OPENAI a cessé de fonctionner après environ 100 requêtes. J’ai essayé plusieurs modèles gratuits tels que smolvlm, Salesforce/blip2-flan-t5-xl et llava-hf/llava-1.5-7b-hf, mais aucun n’a donné de bons résultats, j’ai donc dû obtenir ma propre clé OpenAI.

- Compréhension des données météorologiques sand d'etre expert dans le secteur.

### Améliorations
- Plus de documentation.

- Générer des rapports en français

- Essayer plus des paramètres  pour l'analyze des images.

- Ajouter les locations des personnes dans les rapports.

- Des tests unitaires

- Ajouter +options pour mesurer les models :  précision, rappel, f1... et notament pour **report_agent.py**

- Ajouter +options dans **main.py** avec un script shell