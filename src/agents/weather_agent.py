import os
import json
import logging
from utils.risk_management import detect_risk

logger = logging.getLogger(__name__)


class WeatherAgent:
    def __init__(self, weather_file='assets/weather_info.json', important_airquality=None, important_weather=None):
        self.weather_file = weather_file
        
        self.important_airquality = important_airquality or [
            'pm2_5', 'pm10', 'carbon_monoxide', 'nitrogen_dioxide',
            'sulphur_dioxide', 'ozone', 'ammonia', 'aerosol_optical_depth',
            'uv_index', 'grass_pollen', 'birch_pollen', 'ragweed_pollen',
            'european_aqi', 'us_aqi'
        ]
        
        self.important_weather = important_weather or [
            'temperature_2m', 'apparent_temperature', 'relativehumidity_2m',
            'windspeed_10m', 'windgusts_10m', 'precipitation', 'snowfall',
            'shortwave_radiation', 'soil_moisture_0_to_7cm'
        ]
        
    def load_data(self):
        if not os.path.exists(self.weather_file):
            logger.error(f'[WeatherAgent] Couldn"t find weather data file: {self.weather_file}')
            return {}

        with open(self.weather_file, 'r', encoding='utf-8') as file:
            try:
                return json.load(file)['weather_infos']['1374225']
            except json.JSONDecodeError:
                logger.error('[WeatherAgent] Error in decoding JSON from the weather data file.')
                return {}

    def analyse(self):
        logger.info('[WeatherAgent] Analysing weather data...')
        data = self.load_data()
        if not data:
            return {}

        total_risks = 0

        risk_summary = dict()
        # For each key in the air quality and weather data, check if it is important and if it exceeds the risk threshold.
        for key, val_arr in data['airquality.forecast']['hourly'].items():
            if key in self.important_airquality:
                for ind, val in enumerate(val_arr):
                    if val is not None and detect_risk(key, val):
                        timestamp = data['airquality.forecast']['hourly']['time'][ind]
                        if timestamp not in risk_summary:
                            risk_summary[timestamp] = []
                            risk_summary[timestamp].append(key)
                        risk_summary[timestamp][key] += 1
                        total_risks += 1


        # For each key in the weather data, check if it is important and if it exceeds the risk threshold.
        for key, val_arr in data['forecast']['hourly'].items():
            if key in self.important_weather:
                for ind, val in enumerate(val_arr):
                    if val is not None and detect_risk(key, val):
                        timestamp = data['forecast']['hourly']['time'][ind]
                        if timestamp not in risk_summary:
                            risk_summary[timestamp] = []
                            risk_summary[timestamp].append(key)
                        total_risks += 1

        risk_summary = dict(sorted(risk_summary.items()))
        logger.debug(f'Total risks detected: {total_risks}, Risks Summary: {risk_summary}')
        return {'Total Risks': total_risks, 'Risks Summary': risk_summary}
