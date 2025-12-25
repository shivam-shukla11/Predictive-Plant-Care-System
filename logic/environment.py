# logic/environment.py
from .thresholds import TEMPERATURE_C, HUMIDITY_PERCENT, LIGHT_LUX

def analyze_environment(temperature: float, humidity: float, light: float | None):
    messages = []
    score_delta = 0

    # -------- Temperature --------
    if TEMPERATURE_C["optimal_min"] <= temperature <= TEMPERATURE_C["optimal_max"]:
        messages.append("Temperature is within optimal range")
        score_delta += 5
    elif TEMPERATURE_C["warning_low"] <= temperature <= TEMPERATURE_C["warning_high"]:
        messages.append("Temperature is slightly outside optimal range")
        score_delta -= 5
    else:
        messages.append("Temperature may stress the plant")
        score_delta -= 15

    # -------- Humidity --------
    if HUMIDITY_PERCENT["optimal_min"] <= humidity <= HUMIDITY_PERCENT["optimal_max"]:
        messages.append("Humidity level is healthy")
        score_delta += 5
    elif HUMIDITY_PERCENT["warning_low"] <= humidity <= HUMIDITY_PERCENT["warning_high"]:
        messages.append("Humidity is slightly unbalanced")
        score_delta -= 5
    else:
        messages.append("Humidity may negatively affect plant health")
        score_delta -= 15

    # -------- Light --------
    if light is not None:
        if LIGHT_LUX["optimal_min"] <= light <= LIGHT_LUX["optimal_max"]:
            messages.append("Light exposure is optimal")
            score_delta += 5
        elif LIGHT_LUX["low"] <= light < LIGHT_LUX["optimal_min"]:
            messages.append("Light is slightly low, plant growth may slow")
            score_delta -= 5
        elif light > LIGHT_LUX["optimal_max"] and light <= LIGHT_LUX["high"]:
            messages.append("Light is strong, monitor leaf stress")
            score_delta -= 5
        else:
            messages.append("Light conditions may harm the plant")
            score_delta -= 15

    return {
        "score_delta": score_delta,
        "messages": messages
    }
