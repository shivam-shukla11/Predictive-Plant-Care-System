# logic/trends.py

from datetime import datetime, timedelta
from db import sensor_collection


# -----------------------------------
# Helper: normalize Mongo result
# -----------------------------------
def _round(value):
    return round(value, 2) if value is not None else None


# -----------------------------------
# Last 24 hours (hourly averages)
# -----------------------------------
def get_last_24h_trends():
    since = datetime.utcnow() - timedelta(hours=24)

    pipeline = [
        {
            "$match": {
                "timestamp": {"$gte": since}
            }
        },
        {
            "$group": {
                "_id": {
                    "hour": {
                        "$dateToString": {
                            "format": "%H:00",
                            "date": "$timestamp"
                        }
                    }
                },
                "temperature": {"$avg": "$temperature"},
                "humidity": {"$avg": "$humidity"},
                "soilMoisture": {"$avg": "$soilMoisture"},
                "light": {"$avg": "$light"}
            }
        },
        {"$sort": {"_id.hour": 1}}
    ]

    data = list(sensor_collection.aggregate(pipeline))

    return {
        "labels": [d["_id"]["hour"] for d in data],
        "temperature": [_round(d["temperature"]) for d in data],
        "humidity": [_round(d["humidity"]) for d in data],
        "soilMoisture": [_round(d["soilMoisture"]) for d in data],
        "light": [_round(d["light"]) for d in data],
    }


# -----------------------------------
# Last 7 days (daily averages)
# -----------------------------------
def get_last_7d_trends():
    since = datetime.utcnow() - timedelta(days=7)

    pipeline = [
        {
            "$match": {
                "timestamp": {"$gte": since}
            }
        },
        {
            "$group": {
                "_id": {
                    "day": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$timestamp"
                        }
                    }
                },
                "temperature": {"$avg": "$temperature"},
                "humidity": {"$avg": "$humidity"},
                "soilMoisture": {"$avg": "$soilMoisture"},
                "light": {"$avg": "$light"}
            }
        },
        {"$sort": {"_id.day": 1}}
    ]

    data = list(sensor_collection.aggregate(pipeline))

    return {
        "labels": [d["_id"]["day"] for d in data],
        "temperature": [_round(d["temperature"]) for d in data],
        "humidity": [_round(d["humidity"]) for d in data],
        "soilMoisture": [_round(d["soilMoisture"]) for d in data],
        "light": [_round(d["light"]) for d in data],
    }