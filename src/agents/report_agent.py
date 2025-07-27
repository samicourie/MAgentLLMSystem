import os
import json
import logging
from openai import OpenAI
from dotenv import load_dotenv
from utils.config import REPORT_MODEL, TEMPERATURE, MAX_TOKENS_800, get_test_prompt

load_dotenv()

logger = logging.getLogger(__name__)


class ReportAgent:
    def __init__(self):

        self.llm = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def generate(self, vision_data, weather_data):
        logger.info('[ReportAgent] Generating report with OpenAI...')

        vision_json = json.dumps(vision_data, indent=2, ensure_ascii=False)
        weather_json = json.dumps(weather_data, indent=2, ensure_ascii=False)

        prompt = get_test_prompt(vision_json, weather_json)

        try:
            # Call OpenAI chat completion
            response = self.llm.chat.completions.create(
                model=REPORT_MODEL,
                temperature=TEMPERATURE,
                messages=[
                    {"role": "system", "content": "You are a safety expert for construction sites."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=MAX_TOKENS_800
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f'[ReportAgent] Error during report generation: {e}')
            return '[ReportAgent] Error during report generation.'
        
    def evaluate(self, ai_report, manual_report):

        logger.info('[ReportAgent] Evaluating previously generated report...')

        evaluation_prompt = f'''
            Compare this AI generated report with another report generate manually.

            == AI Report ==
            {ai_report}

            == Manual Report ==
            {str(manual_report)}

            Please rate:
            - Accuracy
            - Coverage
            - Professional tone
            - Relevance of recommendations
            '''

        try:
            response = self.llm.chat.completions.create(
                model=REPORT_MODEL,
                temperature=TEMPERATURE,
                messages=[
                    {"role": "system", "content": "You are a safety expert for construction sites."},
                    {"role": "user", "content": evaluation_prompt}
                ],
                max_tokens=MAX_TOKENS_800
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f'[ReportAgent] Error during report evaluation: {e}')
            return '[ReportAgent] Error during report evaluation.'
