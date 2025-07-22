import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
# from langchain.prompts import ChatPromptTemplate

load_dotenv()

logger = logging.getLogger(__name__)


class ReportAgent:
    def __init__(self):

        '''
        self.llm = ChatOpenAI(
            temperature=0,
            model='gpt-4',
            openai_api_key=os.getenv('OPENAI_API_KEY')
        )
        '''
        self.llm = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def generate(self, vision_data, weather_data, language='fr'):
        logger.info('[ReportAgent] Generating report with OpenAI...')

        if language == 'fr':
            
            prompt = '''
            Vous êtes un expert en sécurité sur les chantiers. Voici des données issues de la vision par caméra et de la météo. Rédigez un rapport clair, structuré, et professionnel sur les risques identifiés.

            === Données de vision ===
            {vision_data}

            === Données météo ===
            {weather_data}

            Générez ensuite des recommandations de sécurité.
            '''
        else:
            prompt = '''
            You are a safety expert for construction sites. Here are data from camera vision and weather. Write a clear, structured, and professional report on the identified risks.

            === Vision Data ===
            {vision_data}

            === Weather Data ===
            {weather_data}

            Then generate safety recommendations.
            '''

        '''
        messages = prompt.format_messages(
            vision=str(vision_data),
            weather=str(weather_data),
        )
        '''
        try:
            # Call OpenAI chat completion
            response = self.llm.chat.completions.create(
                model='gpt-4',
                temperature=0,
                messages=[
                    {"role": "system", "content": "You are a safety expert for construction sites."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f'[ReportAgent] Error during report generation: {e}')
            return '[ReportAgent] Error during report generation.'
        
    def evaluate(self, vision_data, weather_data, generated_report,):
        logger.info('[ReportAgent] Evaluating previously generated report...')

        evaluation_prompt = '''
            Compare this generated report with the input data.

            == Vision Data ==
            {vision_data}

            == Weather Data ==
            {weather_data}

            == Report ==
            {generated_report}

            Please rate:
            - Accuracy
            - Coverage
            - Professional tone
            - Relevance of recommendations
            '''

        '''
        messages = evaluation_prompt.format_messages(
            vision=str(vision_data),
            weather=str(weather_data),
            report = str(generated_report)
        )
        '''
        try:
            response = self.llm.chat.completions.create(
                model='gpt-4',
                temperature=0,
                messages=[
                    {"role": "system", "content": "You are a safety expert for construction sites."},
                    {"role": "user", "content": evaluation_prompt}
                ],
                max_tokens=800
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f'[ReportAgent] Error during report evaluation: {e}')
            return '[ReportAgent] Error during report evaluation.'
        
    
