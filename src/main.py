import logging
from utils.util import combine_data_on_timestamp
from agents.vision_agent import VisionAgent
from agents.report_agent import ReportAgent
from agents.weather_agent import WeatherAgent

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def main():
    logger.info('[MAIN] Launching multi-agent risk analysis system...')
    # Initialisation des agents
    vision_agent = VisionAgent()
    weather_agent = WeatherAgent()
    report_agent = ReportAgent()
    
    # Traitement des données
    # vision_data = vision_agent.analyse()
    vision_data = vision_agent.analyse_old_data('image_predictions_test.json')
    weather_data = weather_agent.analyse()
    
    # Génération de rapport
    report = report_agent.generate(vision_data, weather_data)
    print('\n--- Rapport de Risques ---\n')
    print(report)
    with open('src/output/report.xml', 'w', encoding='utf-8') as file:
        file.write(report)

    manual_report = combine_data_on_timestamp(vision_data, weather_data)
    
    report = report_agent.evaluate(report, manual_report)

    with open('src/output/evaluation.txt', 'w', encoding='utf-8') as file:
        file.write(report)

    print('\n--- Report evaluation ---\n')
    print(report)


if __name__ == '__main__':
    main()
