import os
import requests

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather(lat: float, lon: float) -> dict:
    """
    Fetches current weather data from OpenWeather
    """

    if not OPENWEATHER_API_KEY:
        return {"error": "Weather API key not configured"}

    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"],
            "rain_probability": data.get("rain", {}).get("1h", 0),
            "wind_speed": data["wind"]["speed"]
        }

    except Exception as e:
        return {"error": str(e)}

def get_weather_context(weather: dict | None) -> dict:
    """
    Extracts only plant-relevant signals from raw weather data
    """

    if not weather or "error" in weather:
        return {
            "forecast_temp": None,
            "humidity_forecast": None
        }

    return {
        "forecast_temp": weather.get("temperature"),
        "humidity_forecast": weather.get("humidity")
    }
