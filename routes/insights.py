# routes/insights.py

from fastapi import APIRouter, HTTPException, Depends

from db import sensor_collection
from logic.core.deps import get_current_user
from logic.insights import generate_plant_insights
from logic.weather.client import fetch_weather

router = APIRouter(
    prefix="/plant-insights",
    tags=["Plant Insights"]
)


@router.get("/latest")
def get_latest_plant_insights(
    user: dict = Depends(get_current_user)  # 🔐 AUTH ENFORCED
):
    """
    Fully autonomous plant intelligence endpoint.
    Requires valid JWT access token.
    """

    # 1️⃣ Fetch latest sensor data
    latest = sensor_collection.find_one(
        sort=[("timestamp", -1)],
        projection={"_id": 0}
    )

    if not latest:
        raise HTTPException(
            status_code=404,
            detail="No sensor data found"
        )

    # 2️⃣ Fetch history (last 24 records)
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

    # 3️⃣ Fetch weather (optional)
    weather = None
    if latest.get("lat") is not None and latest.get("lon") is not None:
        weather = fetch_weather(
            lat=latest["lat"],
            lon=latest["lon"]
        )

    # 4️⃣ Generate intelligence
    insights = generate_plant_insights(
        sensor_data=latest,
        history=history,
        weather=weather
    )

    # 5️⃣ Final response
    return {
        "user": {
            "id": user["id"],
            "email": user["email"]
        },
        "timestamp": latest.get("timestamp"),
        "sensor_data": latest,
        "weather": weather,
        "insights": insights
    }