import os
import json


class VisionAgent:
    def __init__(self, assets_path='assets/'):
        self.assets_path = assets_path
        self.metadata_file = os.path.join(self.assets_path, "images_EST-1.json")

    def analyse(self):
        print('[VisionAgent] Analyse the images from the metadata file...')

        if not os.path.exists(self.metadata_file):
            print('[VisionAgent] Couldnt find metadata file:', self.metadata_file)
            return {}

        with open(self.metadata_file, 'r', encoding='utf-8') as file:
            images_metadata = json.load(file)

        images_metadata = images_metadata.get('images', {})

        # A little summary of the risk detection
        risk_summary = {'total_images': len(images_metadata)}

        # Keep track of images with risk labels
        risk_images = set()
        for image_path, image_data in images_metadata.items():
            if 'other' in image_data:
                risk_label = image_data['other']['label']
                if risk_label not in risk_summary:
                    risk_summary[risk_label] = 0
                risk_summary[risk_label] += 1
                risk_images.add(image_path)

        risk_summary['risk_images'] = risk_images
        return risk_summary
