import logging
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

logger = logging.getLogger(__name__)


class ReportAgent:
    def __init__(self, openai_key):
        self.llm = ChatOpenAI(
            temperature=0.4,
            model='gpt-4',  # ou 'gpt-3.5-turbo' si limite
            openai_api_key=openai_key
        )

    def generate(self, vision_data, weather_data, language='fr'):
        logger.info('[ReportAgent] Generating report with OpenAI...')

        if language == 'fr':
            
            prompt = ChatPromptTemplate.from_template('''
            Vous êtes un expert en sécurité sur les chantiers. Voici des données issues de la vision par caméra et de la météo. Rédigez un rapport clair, structuré, et professionnel sur les risques identifiés.

            === Données de vision ===
            {vision}

            === Données météo ===
            {weather}

            Générez ensuite des recommandations de sécurité.
            ''')
        else:
            prompt = ChatPromptTemplate.from_template('''
            You are a safety expert for construction sites. Here are data from camera vision and weather. Write a clear, structured, and professional report on the identified risks.

            === Vision Data ===
            {vision}

            === Weather Data ===
            {weather}

            Then generate safety recommendations.
            ''')

        messages = prompt.format_messages(
            vision=str(vision_data),
            weather=str(weather_data),
        )

        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f'[ReportAgent] Error during report generation: {e}')
            return '[ReportAgent] Error during report generation.'
        
    def evaluate(self, vision_data, weather_data, generated_report,):
        logger.info('[ReportAgent] Evaluating previously generated report...')

        evaluation_prompt = ChatPromptTemplate.from_template(
            '''
            Compare this generated report with the input data.

            == Vision Data ==
            {vision}

            == Weather Data ==
            {weather}

            == Report ==
            {report}

            Please rate:
            - Accuracy
            - Coverage
            - Professional tone
            - Relevance of recommendations
            ''')

        messages = evaluation_prompt.format_messages(
            vision=str(vision_data),
            weather=str(weather_data),
            report = str(generated_report)
        )

        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f'[ReportAgent] Error during report evaluation: {e}')
            return '[ReportAgent] Error during report evaluation.'
        
    
