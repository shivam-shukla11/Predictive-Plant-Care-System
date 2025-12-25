# logic/trend_analysis.py
"""
PHASE 2 — Trend Intelligence Layer

Purpose:
- Analyze recent sensor history
- Detect direction (improving / stable / degrading)
- Generate early warnings BEFORE thresholds are crossed

This file does NOT decide final health score.
It only observes movement over time.
"""

from statistics import mean
from typing import List, Dict

# ----------------------------
# Config (tunable, conservative)
# ----------------------------
MIN_POINTS = 5        # minimum readings to trust trend
NOISE_TOLERANCE = 0.5 # ignore tiny fluctuations


# ----------------------------
# Core trend detector
# ----------------------------
def detect_trend(values: List[float]) -> Dict:
    """
    Detects trend direction using simple slope logic.

    Returns:
        {
            "direction": "improving" | "stable" | "declining",
            "slope": float
        }
    """

    if len(values) < MIN_POINTS:
        return {
            "direction": "insufficient_data",
            "slope": 0.0
        }

    first_half = values[: len(values) // 2]
    second_half = values[len(values) // 2 :]

    avg_start = mean(first_half)
    avg_end = mean(second_half)

    slope = avg_end - avg_start

    if abs(slope) < NOISE_TOLERANCE:
        direction = "stable"
    elif slope > 0:
        direction = "improving"
    else:
        direction = "declining"

    return {
        "direction": direction,
        "slope": round(slope, 2)
    }


# ----------------------------
# Severity classifier
# ----------------------------
def classify_severity(direction: str, slope: float) -> str:
    """
    Converts direction + slope into severity level
    """

    if direction in ("stable", "improving"):
        return "low"

    if abs(slope) > 10:
        return "high"

    return "moderate"


# ----------------------------
# Human-friendly insight
# ----------------------------
def build_message(metric: str, direction: str, severity: str) -> str:
    if direction == "stable":
        return f"{metric} levels are stable"
    if direction == "improving":
        return f"{metric} conditions are improving"
    if direction == "declining":
        if severity == "high":
            return f"{metric} is dropping rapidly — attention recommended"
        return f"{metric} is gradually declining"

    return f"Not enough data to analyze {metric}"


# ----------------------------
# Public API
# ----------------------------
def analyze_trends(history: List[dict]) -> Dict:
    """
    history: list of sensor documents sorted oldest → newest

    Output:
        {
            "soilMoisture": {...},
            "temperature": {...},
            "humidity": {...},
            "light": {...}
        }
    """

    metrics = {
        "soilMoisture": [],
        "temperature": [],
        "humidity": [],
        "light": []
    }

    for doc in history:
        for key in metrics:
            if doc.get(key) is not None:
                metrics[key].append(doc[key])

    results = {}

    for metric, values in metrics.items():
        trend = detect_trend(values)
        severity = classify_severity(trend["direction"], trend["slope"])
        message = build_message(metric, trend["direction"], severity)

        results[metric] = {
            "direction": trend["direction"],
            "severity": severity,
            "slope": trend["slope"],
            "message": message
        }

    return results
