# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from routes.insights import router as insights_router
from routes.auth import router as auth_router
from dotenv import load_dotenv 
from pydantic import BaseModel, Field
from datetime import datetime
from contextlib import asynccontextmanager
from pymongo.errors import PyMongoError
import shutil
import os
# ----------------------
# Database
# ----------------------
from db import sensor_collection
# ----------------------
# Core logic
# ----------------------
from logic import generate_plant_insights
from logic.trends import get_last_24h_trends, get_last_7d_trends
from logic.weather.client import get_weather_context  # ✅ WEATHER

# ----------------------
# AI
# ----------------------
import ai


# ----------------------
# App lifespan
# ----------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        sensor_collection.database.command("ping")
        print("✅ MongoDB connected")
    except Exception as e:
        print("❌ MongoDB connection failed:", e)
        raise RuntimeError("Database not available")

    print("🚀 API started (AI loads lazily)")
    yield
    print("🛑 API shutting down")


app = FastAPI(
    title="Predictive Plant Care System API",
    lifespan=lifespan
)
app.include_router(insights_router, prefix="/api")
app.include_router(auth_router)
# ----------------------
# Health check
# ----------------------
@app.get("/")
def root():
    return {"status": "API is alive"}


# ----------------------
# Sensor schema
# ----------------------
class SensorPayload(BaseModel):
    temperature: float = Field(..., example=24.1)
    humidity: float = Field(..., example=60.2)
    soilMoisture: float = Field(..., example=72.0)
    light: float | None = Field(None, example=800.0)
    device_id: str | None = Field(None, example="esp32-01")
    timestamp: float | None = None  # Unix epoch (optional)


# ----------------------
# Store sensor data
# ----------------------
@app.post("/api/sensor-data", status_code=201)
def receive_sensor_data(payload: SensorPayload):
    try:
        doc = payload.model_dump()

        doc["timestamp"] = (
            datetime.utcfromtimestamp(doc["timestamp"])
            if doc.get("timestamp")
            else datetime.utcnow()
        )

        result = sensor_collection.insert_one(doc)
        return {"status": "ok", "id": str(result.inserted_id)}

    except PyMongoError:
        raise HTTPException(status_code=500, detail="Database error")


# ----------------------
# Latest raw sensor data
# ----------------------
@app.get("/api/latest-data")
def get_latest_sensor_data():
    doc = sensor_collection.find_one(
        sort=[("timestamp", -1)],
        projection={"_id": 0}
    )

    if not doc:
        raise HTTPException(status_code=404, detail="No data found")

    return doc


# ----------------------
# 🌱 Plant insights (CORE FEATURE — Phase 3)
# ----------------------
@app.get("/api/plant-insights/latest")
def get_latest_plant_insights():
    # Latest reading
    latest = sensor_collection.find_one(
        sort=[("timestamp", -1)],
        projection={"_id": 0}
    )

    if not latest:
        raise HTTPException(status_code=404, detail="No sensor data found")

    # History for trends & watering prediction
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

    # 🌤 Weather context (SAFE, OPTIONAL)
    try:
        weather = get_weather_context()
    except Exception:
        weather = None  # weather must NEVER crash insights

    insights = generate_plant_insights(
        sensor_data=latest,
        history=history,
        weather=weather
    )

    return {
        "timestamp": latest["timestamp"],
        "sensor_data": latest,
        "insights": insights
    }


# ----------------------
# 📊 Historical Trends (Graphs-ready)
# ----------------------
@app.get("/api/trends/24h")
def trends_last_24h():
    return get_last_24h_trends()


@app.get("/api/trends/7d")
def trends_last_7d():
    return get_last_7d_trends()


# ----------------------
# 🌿 Disease prediction (AI)
# ----------------------
UPLOAD_DIR = "images"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/api/predict-disease")
async def predict_plant_disease(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return ai.predict_disease(file_path)

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
