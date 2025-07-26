import os 
import logging
from agents.vision_agent import VisionAgent
# from agents.vision_agent_tr import VisionAgent
from agents.weather_agent import WeatherAgent
from agents.report_agent import ReportAgent


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def main():
    logger.info('[MAIN] Launching multi-agent risk analysis system...')
    # Initialisation des agents
    vision_agent = VisionAgent()
    # weather_agent = WeatherAgent()

    report_agent = ReportAgent()
    
    # Traitement des données
    vision_data = vision_agent.analyse()
    # weather_data = weather_agent.analyse()
    
    # Génération de rapport
    # report = report_agent.generate(vision_data, weather_data)
    
    # print('\n--- Rapport de Risques ---\n')
    # print(report)

    # with open('generated_report.txt', 'w', encoding='utf-8') as file:
    #     file.write(str(report))

if __name__ == '__main__':
    main()
