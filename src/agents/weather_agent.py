import os
import json
from utils.risk_management import detect_risk

class WeatherAgent:
    def __init__(self, weather_file='assets/weather_info.json', important_airquality=None, important_weather=None):
        self.weather_file = weather_file
        
        if important_airquality is None:
            self.important_airquality = ['pm2_5', 'pm10', 'carbon_monoxide', 'nitrogen_dioxide',
                                        'sulphur_dioxide', 'ozone', 'ammonia', 'aerosol_optical_depth',
                                        'uv_index', 'grass_pollen', 'birch_pollen', 'ragweed_pollen',
                                        'european_aqi', 'us_aqi']
        
        if important_weather is None:
            self.important_weather = ['temperature_2m', 'apparent_temperature', 'relativehumidity_2m',
                                    'windspeed_10m', 'windgusts_10m', 'precipitation', 'snowfall',
                                    'shortwave_radiation', 'weathercode', 'soil_moisture_0_to_7cm',
                                    'soil_moisture_7_to_28cm']
        
    def load_data(self):
        if not os.path.exists(self.weather_file):
            print('[WeatherAgent] Couldn"t find weather data file.', self.weather_file)
            return {}

        with open(self.weather_file, 'r', encoding='utf-8') as file:
            try:
                return json.load(file)['weather_infos']['1374225']
            except json.JSONDecodeError:
                print('[WeatherAgent] Error in decoding JSON from the weather data file.')
                return []

    def analyse(self):
        print('[WeatherAgent] Analysing weather data...')
        data = self.load_data()
        if not data:
            return {}

        total_risks = 0
        risks = {}
        
        # For each key in the air quality and weather data, check if it is important and if it exceeds the risk threshold.
        for key, val_arr in data['airquality']['hourly'].items():
            if key in self.important_airquality:
                for val in val_arr:
                    if val is not None and detect_risk(key, val):
                        if key not in risks:
                            risks[key] = 0
                        risks[key] += 1
                        total_risks += 1

        # For each key in the weather data, check if it is important and if it exceeds the risk threshold.
        for key, val_arr in data['historical']['hourly'].items():
            if key in self.important_weather:
                for val in val_arr:
                    if val is not None and detect_risk(key, val):
                        if key not in risks:
                            risks[key] = 0
                        risks[key] += 1
                        total_risks += 1
        return {
            'Total Risks': total_risks,
            'Risks': risks
        }
