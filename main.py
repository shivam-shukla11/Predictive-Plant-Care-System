from fastapi import FastAPI
from db import sensor_collection
from pymongo.errors import PyMongoError
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI()

@app.get("/")
def root():
    return {"status": "API is alive"}
# @app.get("/")
# def home():
#     return {"message": "Backend is running"}

# @app.get("/test-db")
# def test_db():
#     doc = {"name": "test", "value": 123}
#     sensor_collection.insert_one(doc)
#     return {"status": "inserted"}


class SensorPayload(BaseModel):
    temperature: float = Field(..., example=24.1)
    humidity: float = Field(..., example=60.2)
    soilMoisture: float = Field(..., example=41.0)
    light: float = Field(None, example=300.0)
    device_id: str = Field(None, example="esp32-01")
    timestamp: float = Field(None, example=None)  # optional Unix epoch in seconds

@app.post("/api/sensor-data", status_code=201)
def receive_sensor_data(payload: SensorPayload):
    doc = payload.dict()
    # if no timestamp provided, set server time
    if not doc.get("timestamp"):
        doc["timestamp"] = datetime.utcnow()
    else:
        # convert epoch seconds to datetime
        try:
            doc["timestamp"] = datetime.utcfromtimestamp(doc["timestamp"])
        except Exception:
            doc["timestamp"] = datetime.utcnow()
    # store in MongoDB
    sensor_collection.insert_one(doc)
    return {"status": "ok", "message": "data stored"}
