"""
FINAL DECISION + NARRATION LAYER
"""

from .hydration import analyze_hydration
from .environment import analyze_environment
from .trend_engine import analyze_trends
from .water_prediction import predict_watering_need


def determine_status_and_message(score: int):
    if score >= 90:
        return "thriving", "Your plant is performing at its best 🌱"
    elif score >= 80:
        return "healthy", "Your plant is healthy and stable"
    elif score >= 70:
        return "stable", "Your plant is doing okay, just keep an eye on it"
    elif score >= 60:
        return "needs_attention", "Your plant may need some care soon"
    else:
        return "critical", "Immediate attention recommended"


def generate_plant_insights(
    sensor_data: dict,
    history: list | None = None,
    weather: dict | None = None
):

    insights: list[str] = []
    health_score: int = 100

    # --- Hydration ---
    hydration = analyze_hydration(sensor_data["soilMoisture"])
    health_score += hydration["score_delta"]
    insights.extend(hydration["messages"])

    # --- Environment ---
    environment = analyze_environment(
        temperature=sensor_data["temperature"],
        humidity=sensor_data["humidity"],
        light=sensor_data.get("light")
    )
    health_score += environment["score_delta"]
    insights.extend(environment["messages"])

    # --- Trends ---
    trend_insights = None
    if history and len(history) >= 5:
        trend_insights = analyze_trends(history)
        for t in trend_insights.values():
            if t["direction"] == "declining":
                insights.append(t["message"])
                if t["severity"] == "high":
                    health_score -= 10
                elif t["severity"] == "moderate":
                    health_score -= 5

    # --- Water prediction ---
    watering = None
    if history and len(history) >= 2:
        watering = predict_watering_need(sensor_data, history)
        insights.append(watering["message"])
        if watering["urgency"] == "high":
            health_score -= 15
        elif watering["urgency"] == "medium":
            health_score -= 8

        # ---------------- Weather context (OPTIONAL) ----------------
    weather_notes = []

    if weather:
        rain_prob = weather.get("rain_probability", 0)
        forecast_temp = weather.get("temperature")
        humidity_forecast = weather.get("humidity")

        # Rain logic
        if rain_prob >= 60:
            weather_notes.append(
                "Rain is likely soon. You may want to delay watering."
            )

            if watering and watering["urgency"] == "high":
                watering["urgency"] = "medium"
                health_score += 5  # soften decision

        # Heat stress
        if forecast_temp is not None and forecast_temp > 35:
            weather_notes.append(
                "High temperatures expected. Soil may dry faster than usual."
            )
            health_score -= 5

        # Dry air stress
        if humidity_forecast is not None and humidity_forecast < 40:
            weather_notes.append(
                "Low outdoor humidity may increase plant stress."
            )
            health_score -= 3


    health_score = max(0, min(int(health_score), 100))
    status, summary = determine_status_and_message(health_score)

    response = {
        "health_score": health_score,
        "status": status,
        "summary": summary,
        "insights": insights
    }

    if trend_insights:
        response["trends"] = trend_insights
    if watering:
        response["watering"] = watering
    if weather_notes:
        response["weather_notes"] = weather_notes

    return response
