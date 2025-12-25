# db.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
if not MONGO_URL:
    raise RuntimeError("MONGO_URL not set in environment")

# Mongo client with sane timeouts
client = MongoClient(
    MONGO_URL,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=5000
)

db = client["plant_db"]
sensor_collection = db["sensor_data"]

sensor_collection.create_index([("timestamp", -1)])
