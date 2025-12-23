from fastapi import FastAPI, UploadFile, File, HTTPException
from db import sensor_collection
from pymongo.errors import PyMongoError
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from contextlib import asynccontextmanager
import shutil
import os

# AI imports
from ai import predict_disease, load_ai

# ----------------------
# Lifespan (startup / shutdown)
# ----------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    load_ai()
    print("API + AI model loaded successfully")
    yield
    print("API shutting down")

app = FastAPI(
    title="Predictive Plant Care System API",
    lifespan=lifespan
)

# ----------------------
# Root health check
# ----------------------
@app.get("/")
def root():
    return {"status": "API is alive"}

# ----------------------
# Sensor data schema
# ----------------------
class SensorPayload(BaseModel):
    temperature: float = Field(..., example=24.1)
    humidity: float = Field(..., example=60.2)
    soilMoisture: float = Field(..., example=41.0)
    light: float | None = Field(None, example=300.0)
    device_id: str | None = Field(None, example="esp32-01")
    timestamp: float | None = Field(None)  # Unix epoch (optional)

# ----------------------
# Store sensor data
# ----------------------
@app.post("/api/sensor-data", status_code=201)
def receive_sensor_data(payload: SensorPayload):
    try:
        doc = payload.model_dump()

        if not doc.get("timestamp"):
            doc["timestamp"] = datetime.now(timezone.utc)
        else:
            doc["timestamp"] = datetime.fromtimestamp(
                doc["timestamp"], tz=timezone.utc
            )

        sensor_collection.insert_one(doc)
        return {"status": "ok", "message": "data stored"}

    except PyMongoError:
        raise HTTPException(status_code=500, detail="Database error")

# ----------------------
# Get latest sensor data ✅ ADDED
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
# AI Disease Prediction
# ----------------------
UPLOAD_DIR = "images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/predict-disease")
async def predict_plant_disease(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = predict_disease(file_path)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
