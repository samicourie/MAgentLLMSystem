def higher_than(value, threshold):
    return value > threshold

def lower_than(value, threshold):
    return value < threshold

def out_of_range(value, low_threshold, high_threshold): 
    return value < low_threshold or value > high_threshold

def higher_than_or_equal(value, threshold):
    return value >= threshold

def lower_than_or_equal(value, threshold):
    return value <= threshold

key_dict = {'pm2_5': {'threshold': 25, 'func': higher_than},
            'pm10': {'threshold': 10000, 'func': higher_than},
            'carbon_monoxide': {'threshold': 200, 'func': higher_than},
            'nitrogen_dioxide': {'threshold': 500, 'func': higher_than},
            'sulphur_dioxide': {'threshold': 180, 'func': higher_than},
            'ozone': {'threshold': 25, 'func': higher_than},
            'ammonia': {'threshold': 1.0, 'func': higher_than},
            'aerosol_optical_depth': {'threshold': 6, 'func': higher_than},
            'uv_index': {'threshold': 50, 'func': higher_than},
            'grass_pollen': {'threshold': 50, 'func': higher_than},
            'birch_pollen': {'threshold': 50, 'func': higher_than},
            'ragweed_pollen': {'threshold': 50, 'func': higher_than},
            'european_aqi': {'threshold': 100, 'func': higher_than},
            'us_aqi': {'threshold': 100, 'func': higher_than},
            'temperature_2m': {'max_threshold': 33, 'min_threshold': 0, 'func': out_of_range},
            'apparent_temperature': {'threshold': 35, 'func': higher_than},
            'relativehumidity_2m': {'threshold': 90, 'func': higher_than},
            'windspeed_10m': {'threshold': 40, 'func': higher_than},
            'windgusts_10m': {'threshold': 50, 'func': higher_than},
            'precipitation': {'threshold': 5, 'func': higher_than},
            'snowfall': {'threshold': 1, 'func': higher_than},
            'shortwave_radiation': {'threshold': 700, 'func': higher_than},
            'weathercode': {'threshold': 50, 'func': higher_than_or_equal},
            'soil_moisture_0_to_7cm': {'max_threshold': 0.5, 'min_threshold': 0.1, 'func': out_of_range}}

def detect_risk(key, val):
    if key in key_dict:
        threshold_info = key_dict[key]
        if 'max_threshold' in threshold_info:
            return threshold_info['func'](val, threshold_info['min_threshold'], threshold_info['max_threshold'])
        else:
            return threshold_info['func'](val, threshold_info['threshold'])
    return False
