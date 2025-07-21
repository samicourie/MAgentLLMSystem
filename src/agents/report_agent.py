from utils.config import OPENAI_KEY
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


class ReportAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.4,
            model='gpt-4',  # ou 'gpt-3.5-turbo' si limite
            openai_api_key=OPENAI_KEY
        )

    def generate(self, vision_data, weather_data, language='fr'):
        print('[ReportAgent] Generating report with OpenAI...')

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

        response = self.llm(messages)
        return response.content
