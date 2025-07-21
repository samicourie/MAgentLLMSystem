# Airquality functions for risk detection
def fine_particles_pm2_5(value, threshold=25):
    return value > threshold
def coarse_particles_pm10(value, threshold=50):
    return value > threshold
def carbon_monoxide(value, threshold=10000):
    return value > threshold
def nitrogen_dioxide(value, threshold=200):
    return value > threshold
def sulphur_dioxide(value, threshold=500):
    return value > threshold
def ozone(value, threshold=180):
    return value > threshold
def ammonia(value, threshold=25):
    return value > threshold
def aerosol_optical_depth(value, threshold=1.0):
    return value > threshold
def ultraviolet_index(value, threshold=6):
    return value > threshold
def grass_pollen(value, threshold=50):
    return value > threshold
def birch_pollen(value, threshold=50):
    return value > threshold
def ragweed_pollen(value, threshold=50):
    return value > threshold
def european_aqi(value, threshold=100):
    return value > threshold
def us_aqi(value, threshold=100):
    return value > threshold

# Weather functions for risk detection
def heat(value, max_threshold=33, min_threshold=0):
    return value > max_threshold or value < min_threshold
def thermal_stress(value, threshold=35):
    return value > threshold
def excessive_humidity(value, threshold=90):
    return value > threshold
def sustained_wind(value, threshold=40):
    return value > threshold
def dangerous_gusts(value, threshold=50):
    return value > threshold
def intense_rain(value, threshold=5):
    return value > threshold
def snowfall(value, threshold=1):
    return value > threshold
def strong_solar_radiation(value, threshold=700):
    return value > threshold
def severe_weather_conditions(value, threshold=50):
    return value >= threshold
def unstable_soil(value, high_threshold=0.5, low_threshold=0.1):
    return value < low_threshold or value > high_threshold

key_dict = {'pm2_5': fine_particles_pm2_5,
            'pm10': coarse_particles_pm10,
            'carbon_monoxide': carbon_monoxide,
            'nitrogen_dioxide': nitrogen_dioxide,
            'sulphur_dioxide': sulphur_dioxide,
            'ozone': ozone,
            'ammonia': ammonia,
            'aerosol_optical_depth': aerosol_optical_depth,
            'uv_index': ultraviolet_index,
            'grass_pollen': grass_pollen,
            'birch_pollen': birch_pollen,
            'ragweed_pollen': ragweed_pollen,
            'european_aqi': european_aqi,
            'us_aqi': us_aqi,
            'temperature_2m': heat,
            'apparent_temperature': thermal_stress,
            'relativehumidity_2m': excessive_humidity,
            'windspeed_10m': sustained_wind,
            'windgusts_10m': dangerous_gusts,
            'precipitation': intense_rain,
            'snowfall': snowfall,
            'shortwave_radiation': strong_solar_radiation,
            'weathercode': severe_weather_conditions,
            'soil_moisture_0_to_7cm': unstable_soil}

def detect_risk(key, val):
    if key in key_dict:
        return key_dict[key](val)
    return False
