from agents.vision_agent import VisionAgent
from agents.weather_agent import WeatherAgent
from agents.report_agent import ReportAgent


def main():
    print('[INFO] Lancement du système multi-agent d"analyse des risques...')
    
    # Initialisation des agents
    vision_agent = VisionAgent()
    weather_agent = WeatherAgent()
    report_agent = ReportAgent()
    
    # Traitement des données
    vision_data = vision_agent.analyse()
    weather_data = weather_agent.analyse()
    
    # Génération de rapport
    report = report_agent.generate(vision_data, weather_data)
    
    print('\n--- Rapport de Risques ---\n')
    print(report)

if __name__ == '__main__':
    main()
