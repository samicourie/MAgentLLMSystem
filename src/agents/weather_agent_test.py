import os
import json
from utils.config import OPENAI_KEY
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


class WeatherAgent:
    def __init__(self, weather_file='assets/weather_info.json'):
        self.weather_file = weather_file
        self.llm = ChatOpenAI(
            model='gpt-4',
            temperature=0.3,
            openai_api_key=OPENAI_KEY
        )

        self.airquality_keys = ['carbon_monoxide', 'nitrogen_dioxide', 'sulphur_monoxide', 'ozone', 'pm10', 'pm2_5']
        self.weather_keys = ['temperature_2m', 'apparent_temperature', 'cloudcover_low', 'windspeed_10m', 'windspeed_100m',
                            'shortwave_radiation', 'precipitation', 'direct_radiation']

    def load_weather_data(self):
        if not os.path.exists(self.weather_file):
            print('[WeatherAgent] Fichier météo introuvable.')
            return []

        with open(self.weather_file, 'r', encoding='utf-8') as file:
            try:
                weather_data = json.load(file)
                weather_data = weather_data['weather_infos']['1374225']
                '''
                filtered_data = {'airquality': dict(), 'weather': dict()}
                filtered_data['airquality']['units'] = weather_data['airquality']['hourly_units']
                filtered_data['airquality']['values'] = dict()
                for key, val in weather_data['airquality']['hourly'].items():
                    # Limiter à 3 jours
                    if key in self.airquality_keys:
                        filtered_data['airquality']['values'][key] = val[:72]

                filtered_data['weather']['units'] = weather_data['historical']['hourly_units']
                filtered_data['weather']['values'] = dict()
                for key, val in weather_data['historical']['hourly'].items():
                    # Limiter à 3 jours
                    if key in self.weather_keys:
                        filtered_data['weather']['values'][key] = val[:72]

                return filtered_data
                '''
                return weather_data
            except json.JSONDecodeError:
                print('[WeatherAgent] Erreur JSON dans weather.json.')
                return []

    def analyze(self):
        print('[WeatherAgent] Analyse des données météo...')

        weather_data = self.load_weather_data()

        important_measures = self.get_important_measures(weather_data)
        # Résumer les risques météo (simplifié)
        wind_risks = [entry for entry in weather_data if entry.get('wind_speed', 0) > 40]
        heavy_rain = [entry for entry in weather_data if entry.get('rain_mm', 0) > 10]

        return {
            'days_analyzed': len(weather_data),
            'high_wind_days': len(wind_risks),
            'rainy_days': len(heavy_rain),
        }
    

    def get_important_measures(self, weather_data):
        print('[WeatherAgent] Extraction des mesures importantes...')

        airquality_keys = ', '.join(weather_data['airquality']['hourly'].keys())
        weather_keys = ', '.join(weather_data['historical']['hourly'].keys())

        prompt = ChatPromptTemplate.from_template('''
            Tu es un expert en météorologie sur un chantier de construction. 
            Voici des noms de mesures importantes pour la qualité de l'air et la météo :
            - Air quality : {airquality_keys}
            - Weather : {weather_keys}

            Ta tâche est de :
            - Identifier les mesures les plus importants
            - Retourner un **JSON** avec chaque mesure et ses valeurs de risque comme ceci:

            {{
                'ozone': 180,
                'windspeed_10m': 10,
                ...

            }}
            ''')
        
        messages = prompt.format_messages(airquality_keys=airquality_keys, weather_keys=weather_keys)
        response = self.llm(messages)

        return response

"""
    def analyze(self):
        print('[WeatherAgent] Analyse via LLM...')

        weather_data = self.load_weather_data()
        if not weather_data:
            return {}

        prompt = ChatPromptTemplate.from_template('''
            Tu es un expert en météorologie sur un chantier de construction. 
            Voici des données brutes météo par heure, sous forme de JSON.

            Ta tâche est de :
            - Identifier les **cas où il y a un risque météo**
            - Classer ces risques par type : heavy_rain, high_wind, extreme_heat, low_visibility, ozone_alert, etc.
            - Retourner un **résumé JSON** comme ceci :

            {{
            'total_risks': <total>,
            'risks_by_type': {{
                'heavy_rain': <count>,
                'high_wind': <count>,
                ...
            }}
            }}

            Voici les données météo en format json pour la quality d'air "airquality" et le forecast "forecast" :
            {weather_json}
            ''')

        input_text = json.dumps(weather_data)  # limiter si fichier très gros
        messages = prompt.format_messages(weather_json=input_text)
        response = self.llm(messages)

        try:
            # Essayons de parser sa réponse comme JSON
            return json.loads(response.content)
        except json.JSONDecodeError:
            print('[WeatherAgent] Réponse LLM non JSON, contenu brut :')
            print(response.content)
            return {'raw_output': response.content}
"""
