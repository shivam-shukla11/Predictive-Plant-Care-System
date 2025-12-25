# logic/trends.py
from datetime import datetime, timedelta
from db import sensor_collection

def get_last_24h_trends():
    since = datetime.utcnow() - timedelta(hours=24)

    pipeline = [
        {"$match": {"timestamp": {"$gte": since}}},
        {
            "$group": {
                "_id": {
                    "hour": {"$hour": "$timestamp"}
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
        "labels": [f"{d['_id']['hour']}:00" for d in data],
        "temperature": [round(d["temperature"], 2) for d in data],
        "humidity": [round(d["humidity"], 2) for d in data],
        "soilMoisture": [round(d["soilMoisture"], 2) for d in data],
        "light": [round(d["light"], 2) for d in data],
    }


def get_last_7d_trends():
    since = datetime.utcnow() - timedelta(days=7)

    pipeline = [
        {"$match": {"timestamp": {"$gte": since}}},
        {
            "$group": {
                "_id": {
                    "day": {"$dayOfMonth": "$timestamp"}
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
        "labels": [f"Day {d['_id']['day']}" for d in data],
        "temperature": [round(d["temperature"], 2) for d in data],
        "humidity": [round(d["humidity"], 2) for d in data],
        "soilMoisture": [round(d["soilMoisture"], 2) for d in data],
        "light": [round(d["light"], 2) for d in data],
    }
