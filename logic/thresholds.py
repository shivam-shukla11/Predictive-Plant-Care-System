# logic/thresholds.py

# Temperature in °C (India-friendly averages)
TEMPERATURE_C = {
    "optimal_min": 22,
    "optimal_max": 32,
    "warning_low": 18,
    "warning_high": 36
}

# Relative Humidity %
HUMIDITY_PERCENT = {
    "optimal_min": 45,
    "optimal_max": 70,
    "warning_low": 35,
    "warning_high": 85
}

# Soil moisture as % (capacitive sensor normalized)
# These names MATCH hydration + water prediction logic
SOIL_MOISTURE_PERCENT = {
    "well_hydrated": 75,   # happy, no action
    "healthy": 60,         # safe zone
    "watch": 45,           # early warning
    "pre_dry": 35,         # watering soon
    "dry": 25              # water now
}

# Light in LUX (generic indoor plants)
LIGHT_LUX = {
    "low": 300,
    "optimal_min": 500,
    "optimal_max": 2000,
    "high": 3000
}
