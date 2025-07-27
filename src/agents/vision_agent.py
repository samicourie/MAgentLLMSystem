import os
import json
import time
import logging
from collections import Counter

from PIL import Image
from dotenv import load_dotenv
from openai import OpenAI
from utils.util import convert_image_to_base64, split_image, parse_llm_response
from utils.config import PROMPT, RESOLUTION, LLM_MODEL, TEMPERATURE, MAX_TOKENS_600

load_dotenv()

logger = logging.getLogger(__name__)


class VisionAgent:
    def __init__(self, assets_path='assets', image_folder='images_EST_GT', metadata_file='images_EST_GT.json'):
        self.assets_path = assets_path
        self.image_folder = os.path.join(self.assets_path, image_folder)
        self.metadata_file = os.path.join(self.assets_path, metadata_file)

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

        result = {}
        for image_obj in images_metadata:
            timestamp = image_obj['timestamp']
            image_path = image_obj['image_path']
            detections = image_obj['detections']
            new_detections = []

            for det_obj in detections:
                if 'no-ppe' in det_obj and det_obj['no-ppe']['prediction'] == '1':
                    new_detections.append('No PP Equipment')
                    continue
                for key in ['has-hard-hat', 'has-high-vis-pants', 'has-high-vis-vest']:
                    if key in det_obj and det_obj[key]['prediction'] == '0':
                        new_detections.append(key.replace('has-', 'no-').replace('-', ' ').title())

            if len(new_detections) > 0:
                if timestamp not in result:
                    result[timestamp] = []
                result[timestamp].append({
                    'image_path': image_path,
                    'Risks': dict(Counter(new_detections))
                })

        return {'Risks Summary': result, 'Total Detections': len(images_metadata)}

    def analyse_image(self, image):
        
        response = self.vision_llm.chat.completions.create(
        model=LLM_MODEL,
        temperature=TEMPERATURE,
        messages=[
            {'role': 'system', 'content': 'You are a construction safety expert.'},
            {
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': PROMPT},
                    {
                        'type': 'image_url',
                        'image_url': {
                            'url': f'data:image/jpeg;base64,{image}', 'detail': RESOLUTION
                        }
                    }
                ]
            }
        ],
        max_tokens=MAX_TOKENS_600,
        )

        return response.choices[0].message.content

    def analyse(self, output_file='image_predictions_test.json'):
        logger.info('[VisionAgent] Analysing images from metadata file & images...')
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

        logger.info(f'[VisionAgent] Saving predictions to {output_file}')
        with open(os.path.join(self.assets_path, output_file), 'w', encoding='utf-8') as file:
            json.dump({'images': new_images, 'LLM Failure': llm_fails}, file)

        # Return a summary of the risks detected
        return self._summarize_risks(new_images)

    def analyse_old_data(self, input_file='image_predictions_test.json'):
        logger.info('[VisionAgent] Analysing meta informtion of previously tested images...')

        with open(os.path.join(self.assets_path, input_file), 'r', encoding='utf-8') as file:
            data = json.load(file)
            if 'images' not in data:
                logger.error(f'[VisionAgent] No images found in {input_file}')
                return {}
        
        
        # Return a summary of the risks detected
        return self._summarize_risks(data['images'])
