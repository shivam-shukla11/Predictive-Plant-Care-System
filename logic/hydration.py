# logic/hydration.py
from .thresholds import SOIL_MOISTURE_PERCENT

def analyze_hydration(soil_moisture: float):
    messages = []
    score_delta = 0

    # well_hydrated (75+) or healthy (60+)
    if soil_moisture >= SOIL_MOISTURE_PERCENT["well_hydrated"]:
        messages.append("Soil moisture is in the optimal range")
        score_delta += 5

    elif soil_moisture >= SOIL_MOISTURE_PERCENT["healthy"]:
        messages.append("Soil moisture is healthy")
        score_delta += 0

    elif soil_moisture >= SOIL_MOISTURE_PERCENT["watch"]:
        messages.append("Soil moisture is slightly low, keep monitoring")
        score_delta -= 5

    elif soil_moisture >= SOIL_MOISTURE_PERCENT["pre_dry"]:
        messages.append("Soil moisture is low, watering may be needed soon")
        score_delta -= 15

    else:  # below pre_dry (dry zone)
        messages.append("Soil moisture is critically low, watering recommended")
        score_delta -= 30

    return {
        "score_delta": score_delta,
        "messages": messages
    }
