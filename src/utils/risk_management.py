import logging

logger = logging.getLogger(__name__)


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


# Thresholds are example values; adjust based on domain knowledge or regulations
key_dict = {
    'pm2_5': {'threshold': 25, 'func': higher_than},  # µg/m³, WHO guideline
    'pm10': {'threshold': 100, 'func': higher_than},
    'carbon_monoxide': {'threshold': 200, 'func': higher_than},  # ppm or µg/m³
    'nitrogen_dioxide': {'threshold': 500, 'func': higher_than},
    'sulphur_dioxide': {'threshold': 180, 'func': higher_than},
    'ozone': {'threshold': 180, 'func': higher_than},
    'ammonia': {'threshold': 25, 'func': higher_than},
    'aerosol_optical_depth': {'threshold': 6, 'func': higher_than},
    'uv_index': {'threshold': 50, 'func': higher_than},
    'grass_pollen': {'threshold': 50, 'func': higher_than},
    'birch_pollen': {'threshold': 50, 'func': higher_than},
    'ragweed_pollen': {'threshold': 50, 'func': higher_than},
    'european_aqi': {'threshold': 100, 'func': higher_than},
    'us_aqi': {'threshold': 100, 'func': higher_than},
    
    'temperature_2m': {'min_threshold': 0, 'max_threshold': 33, 'func': out_of_range},  # Celsius
    'apparent_temperature': {'threshold': 35, 'func': higher_than},
    'relativehumidity_2m': {'threshold': 90, 'func': higher_than},  # percent
    'windspeed_10m': {'threshold': 40, 'func': higher_than},  # km/h or m/s (specify!)
    'windgusts_10m': {'threshold': 50, 'func': higher_than},
    'precipitation': {'threshold': 5, 'func': higher_than},  # mm/h or mm/day (specify!)
    'snowfall': {'threshold': 1, 'func': higher_than},
    'shortwave_radiation': {'threshold': 700, 'func': higher_than},
    'weathercode': {'threshold': 50, 'func': higher_than_or_equal},  # unclear what this encodes
    'soil_moisture_0_to_7cm': {'min_threshold': 0, 'max_threshold': 5, 'func': out_of_range}
}


def detect_risk(key, val):
    if val is None:
        return False

    if key not in key_dict:
        logger.warning(f'Unknown key for risk detection: {key}')
        return False

    thresholds = key_dict[key]
    func = thresholds.get('func')

    if func is None:
        logger.warning(f'No function defined for key: {key}')
        return False

    if 'min_threshold' in thresholds and 'max_threshold' in thresholds:
        return func(val, thresholds['min_threshold'], thresholds['max_threshold'])
    elif 'threshold' in thresholds:
        return func(val, thresholds['threshold'])
    else:
        logger.warning(f'No thresholds found for key: {key}')
        return False
