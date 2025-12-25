"""
water_prediction.py
-------------------
Rule-based watering prediction engine.

Purpose:
- Predict WHEN watering will be needed (not exact quantity)
- Be conservative (no panic alerts)
- Use trend + environment, not just one reading

This is Phase-2 intelligence (pre-ML).
"""

from datetime import datetime
from typing import List, Dict


# ----------------------
# Tunable constants
# ----------------------

# Soil moisture bands (%)
SOIL_BANDS = {
    "well_hydrated": 60,
    "healthy": 45,
    "watch": 35,
    "pre_dry": 25
}

# Drying speed thresholds (% drop per 24h)
FAST_DRY_DROP = 8     # aggressive drying
SLOW_DRY_DROP = 3     # stable soil

# Environmental stress thresholds
TEMP_HIGH = 32        # °C
HUMIDITY_LOW = 40     # %
LIGHT_HIGH = 800      # lux


# ----------------------
# Helper: calculate moisture drop
# ----------------------
def calculate_moisture_drop(history: List[Dict]) -> float:
    """
    Calculates percentage drop in soil moisture
    using oldest vs latest value in history window.
    """

    if len(history) < 2:
        return 0.0

    # Handle both camelCase and snake_case keys
    start = history[0].get("soilMoisture") or history[0].get("soil_moisture", 0)
    end = history[-1].get("soilMoisture") or history[-1].get("soil_moisture", 0)

    return max(start - end, 0.0)


# ----------------------
# Helper: environmental risk score
# ----------------------
def environmental_risk(latest: Dict) -> int:
    """
    Returns a drying risk score (0–3)
    """

    risk = 0

    if latest["temperature"] > TEMP_HIGH:
        risk += 1

    if latest["humidity"] < HUMIDITY_LOW:
        risk += 1

    if latest.get("light") and latest["light"] > LIGHT_HIGH:
        risk += 1

    return risk


# ----------------------
# Main prediction logic
# ----------------------
def predict_watering_need(
    latest: Dict,
    history: List[Dict]
) -> Dict:
    """
    Predicts watering requirement.

    Inputs:
        latest  → latest sensor reading
        history → recent readings (last 24h)

    Output:
        dict with calm, user-friendly decision
    """

    soil = latest["soilMoisture"]
    drop_24h = calculate_moisture_drop(history)
    risk = environmental_risk(latest)

    # ----------------------
    # Decision logic
    # ----------------------

    # 🚨 Dry now
    if soil < SOIL_BANDS["pre_dry"]:
        return {
            "needs_water": True,
            "urgency": "high",
            "next_check_in_hours": 2,
            "message": "Soil is dry. Watering is recommended now."
        }

    # ⚠️ Pre-dry + risky environment
    if soil < SOIL_BANDS["watch"] and (drop_24h >= FAST_DRY_DROP or risk >= 2):
        return {
            "needs_water": True,
            "urgency": "medium",
            "next_check_in_hours": 6,
            "message": "Soil moisture is dropping. Watering may be needed soon."
        }

    # 👀 Watch zone (calm warning)
    if soil < SOIL_BANDS["healthy"]:
        return {
            "needs_water": False,
            "urgency": "low",
            "next_check_in_hours": 12,
            "message": "Soil moisture is slightly low. Monitor the plant."
        }

    # 🌱 Healthy & stable
    if drop_24h <= SLOW_DRY_DROP and risk == 0:
        return {
            "needs_water": False,
            "urgency": "none",
            "next_check_in_hours": 24,
            "message": "Soil moisture is healthy. No watering needed today."
        }

    # 🌤 Default safe state
    return {
        "needs_water": False,
        "urgency": "none",
        "next_check_in_hours": 18,
        "message": "Plant is stable. Check again later."
    }
