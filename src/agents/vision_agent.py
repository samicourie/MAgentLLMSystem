import os
import json
import time
import logging
from PIL import Image
from dotenv import load_dotenv
from openai import OpenAI
from utils.util import convert_image_to_base64, split_image, parse_llm_response

load_dotenv()

logger = logging.getLogger(__name__)


class VisionAgent:
    def __init__(self, assets_path='assets', image_folder='images_EST_GT', metadata_file='images_EST_GT.json'):
        self.assets_path = assets_path
        self.image_folder = os.path.join(self.assets_path, image_folder)
        self.metadata_file = os.path.join(self.assets_path, metadata_file)

        # self.vision_llm = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.vision_llm = OpenAI(api_key=os.getenv('MY_OPENAI_API_KEY'))

    def _load_metadata(self):
        if not os.path.exists(self.metadata_file):
            logger.error(f'[VisionAgent] Metadata file not found: {self.metadata_file}')
            return {}

        with open(self.metadata_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                return data
            except json.JSONDecodeError:
                logger.error('[VisionAgent] Failed to decode JSON.')
                return {}
            
    def _summarize_risks(self, images_metadata):
        summary = {'Total Detections': len(images_metadata)}
        risk_summary = {'has-hard-hat': 0, 'has-high-vis-pants': 0, 'has-high-vis-vest': 0, 'no-ppe': 0}
        risk_timestamps = set()
        for item in images_metadata:
            for key in risk_summary:
                value = item[key]
                if value['prediction'] == '1':
                    risk_summary[key] += 1
                    risk_timestamps.add(item['timestamp'])


        summary['Risk Summary'] = list(risk_summary)
        summary['Risk Dates'] = list(risk_timestamps)
        return summary

    def analyse_image(self, image):
        
        response = self.vision_llm.chat.completions.create(
        model='gpt-4o-mini',
        # model='gpt-4-turbo',
        temperature=0,
        messages=[
            {'role': 'system', 'content': 'You are a construction safety expert.'},
            {
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': '''You are an AI safety inspector. You are shown a construction site image.

Your only task is to check if the person in the image is wearing any of the following PPE (personal protective equipment):

- A hard hat
- A high-visibility vest
- High-visibility pants
- No PPE at all

Only include items in the output if the model's confidence is greater than 0.5.  
If confidence is ≤ 0.5, set `<prediction>` to 0 and still include the actual confidence value.
Predictions must be based only on visual evidence in the image. Do not assume PPE is present unless it is clearly visible with confidence > 0.5.
Please respond using **only** the following XML structure. Do not include any extra text, explanation, or summaries. Return only the content starting with <output> and ending with </output>.

<output>
    <has-hard-hat>
        <prediction>{1 or 0}</prediction>
        <confidence>{0.0 - 1.0}</confidence>
    </has-hard-hat>
    <has-high-vis-pants>
        <prediction>{1 or 0}</prediction>
        <confidence>{0.0 - 1.0}</confidence>
    </has-high-vis-pants>
    <has-high-vis-vest>
        <prediction>{1 or 0}</prediction>
        <confidence>{0.0 - 1.0}</confidence>
    </has-high-vis-vest>
    <no-ppe>
        <prediction>{1 or 0}</prediction>
        <confidence>{0.0 - 1.0}</confidence>
    </no-ppe>
</output>'''},
                    {
                        'type': 'image_url',
                        'image_url': {
                            'url': f'data:image/jpeg;base64,{image}', 'detail': 'high'
                        }
                    }
                ]
            }
        ],
        max_tokens=500,
        )

        return response.choices[0].message.content

    def analyse(self):
        logger.info('[VisionAgent] Analysing images from metadata file...')
        metadata_file = self._load_metadata()
        if not metadata_file:
            return {}

        images = metadata_file['images']
        llm_fails = 0
        new_images = []
        for image_path, img_obj in images.items():
            predictions = []
            print(image_path, llm_fails)
            img = Image.open(os.path.join(self.image_folder, image_path))
            for d_obj in img_obj['detections']:
                cropped_image = split_image(img, d_obj['bounding_box_start_x'], d_obj['bounding_box_end_x'],
                                            d_obj['bounding_box_start_y'], d_obj['bounding_box_end_y'])
                cropped_img_64 = convert_image_to_base64(cropped_image)
                try:
                    img_info = self.analyse_image(cropped_img_64)
                    pred = parse_llm_response(img_info)
                    predictions.append(pred)
                except Exception as _:
                    predictions.append('-1')
                    llm_fails += 1
                # time.sleep(5)  # To avoid hitting rate limits
            json_info = {
                'timestamp': img_obj['timestamp'],
                'image_path': image_path,
                'detections': predictions
            }
            new_images.append(json_info)
            with open(self.assets_path + '/image_predictions_promt_2.json', 'w', encoding='utf-8') as file:
                json.dump({'images': new_images, 'LLM Failure': llm_fails}, file)

        logger.info(f'[VisionAgent] Saving predictions to assets/image_predictions_promt_2.json')
        with open(self.assets_path + '/image_predictions_promt_2.json', 'w', encoding='utf-8') as file:
            json.dump({'images': new_images, 'LLM Failure': llm_fails}, file)
        
        '''
        risk_summary = self._summarize_risks(predictions)
        risk_summary['LLM Failure'] = llm_fails

        logger.debug(f'[VisionAgent] Risk summary: {risk_summary}')
        
        return risk_summary
        '''
