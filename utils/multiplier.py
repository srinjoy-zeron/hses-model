from constants.multiplier import ENVIRONMENTAL_FACTOR_MAPPINGS
from api.imports import datetime
from .mappings import Mapping_Class

def time_of_day_multiplier(time_str):
    if time_str is None : 
        return 1.0

    minutes = datetime.strptime(time_str, "%H:%M").hour * 60 + datetime.strptime(time_str, "%H:%M").minute

    if minutes is None : 
        return 1.0

    if 420 <= minutes < 780:      # 7am–1pm
        return 0.8
    elif 780 <= minutes < 960:    # 1pm–4pm
        return 1.15
    elif 960 <= minutes < 1260:   # 4pm–9pm
        return 1.05
    else:                 # late night
        if(minutes < 420) :
          # not to be confused with session length
          minutes += 24 * 60 - 21 * 60 # agar midnight cross hua hai then
        else :
          minutes -= 21 * 60 # agar nahi hua hai
        return min(1.3, 1.05 + (minutes) / 600)


def session_length_multiplier(minutes : int):
    if minutes is None : 
        return 1.0
    if minutes <= 50:
        return 0.8
    elif minutes <= 90:
        return 1.0
    return min(1.25, 2 ** (0.001 * minutes))


def noise_environment_multiplier(noise_score : int , environmental_factor : str):
    if noise_score is None : 
        noise_score = 0
    noise_score = min(130 , noise_score) # upper limiting x for unnatural values for scaling factors
    noise_factor = 2 ** (0.015 * max(0 , noise_score - 76))

    multiplier_mapping_obj = Mapping_Class(ENVIRONMENTAL_FACTOR_MAPPINGS)
    env_factor = multiplier_mapping_obj.map(environmental_factor)

    return (noise_factor + env_factor) / 2