import os
import json
import logging

logger = logging.getLogger(__name__)


class VisionAgent:
    def __init__(self, assets_path='assets/'):
        self.assets_path = assets_path
        self.metadata_file = os.path.join(self.assets_path, "images_EST-1.json")

    def _load_metadata(self):
        if not os.path.exists(self.metadata_file):
            logger.error(f'[VisionAgent] Metadata file not found: {self.metadata_file}')
            return {}

        with open(self.metadata_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                return data.get('images', {})
            except json.JSONDecodeError:
                logger.error('[VisionAgent] Failed to decode JSON.')
                return {}
            
    def _summarize_risks(self, images_metadata):
        summary = {'total_images': len(images_metadata)}
        risk_images = set()

        for image_path, image_data in images_metadata.items():
            label = image_data.get('other', {}).get('label')
            if label:
                summary[label] = summary.get(label, 0) + 1
                risk_images.add(image_path)

        summary['risk_images'] = list(risk_images)
        return summary

    def analyse(self):
        logger.info('[VisionAgent] Analysing images from metadata file...')
        metadata = self._load_metadata()
        if not metadata:
            return {}

        risk_summary = self._summarize_risks(metadata)

        logger.debug(f'Risk summary: {risk_summary}')
        return risk_summary
