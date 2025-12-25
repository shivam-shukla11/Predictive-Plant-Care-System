# routes/insights.py

from fastapi import APIRouter, HTTPException
from db import sensor_collection
from logic.insights import generate_plant_insights
from logic.weather.client import fetch_weather

router = APIRouter()


@router.get("/plant-insights/latest")
def get_latest_plant_insights():
    """
    Fully autonomous plant intelligence endpoint.
    Backend decides everything.
    """

    # 1️⃣ Latest sensor data
    latest = sensor_collection.find_one(
        sort=[("timestamp", -1)],
        projection={"_id": 0}
    )

    if not latest:
        raise HTTPException(status_code=404, detail="No sensor data found")

    # 2️⃣ History (for trends + watering)
    history_cursor = sensor_collection.find(
        {},
        projection={
            "_id": 0,
            "temperature": 1,
            "humidity": 1,
            "soilMoisture": 1,
            "light": 1,
            "timestamp": 1
        }
    ).sort("timestamp", 1).limit(24)

    history = list(history_cursor)

    # 3️⃣ Weather (optional, safe)
    weather = None
    if latest.get("lat") is not None and latest.get("lon") is not None:
        weather = fetch_weather(
            lat=latest["lat"],
            lon=latest["lon"]
        )

    # 4️⃣ Intelligence
    insights = generate_plant_insights(
        sensor_data=latest,
        history=history,
        weather=weather
    )

    # 5️⃣ Final response
    return {
        "timestamp": latest.get("timestamp"),
        "sensor_data": latest,
        "weather": weather,
        "insights": insights
    }
