"""
Weather API tools for fetching weather data from OpenWeatherMap
"""

import os
import requests
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5"


def get_current_weather(city: str, country_code: Optional[str] = None) -> Dict[str, Any]:
    """
    Get current weather for a city.

    Args:
        city: City name (e.g., "Paris", "Lyon", "New York")
        country_code: Optional 2-letter country code (e.g., "FR", "US")

    Returns:
        Dictionary with weather information including:
        - temperature (current, feels_like, min, max)
        - conditions (description, main)
        - humidity, wind_speed, clouds
        - timestamp
    """
    if not OPENWEATHER_API_KEY:
        return {"error": "OPENWEATHER_API_KEY not configured"}

    # Build location query
    location = f"{city},{country_code}" if country_code else city

    try:
        # Call OpenWeatherMap API
        response = requests.get(
            f"{BASE_URL}/weather",
            params={
                "q": location,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric",  # Celsius
                "lang": "fr"  # French descriptions
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        # Parse and structure the response
        weather_info = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "timestamp": datetime.fromtimestamp(data["dt"]).isoformat(),
            "temperature": {
                "current": round(data["main"]["temp"], 1),
                "feels_like": round(data["main"]["feels_like"], 1),
                "min": round(data["main"]["temp_min"], 1),
                "max": round(data["main"]["temp_max"], 1)
            },
            "conditions": {
                "main": data["weather"][0]["main"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"]
            },
            "humidity": data["main"]["humidity"],
            "wind_speed": round(data["wind"]["speed"] * 3.6, 1),  # m/s to km/h
            "clouds": data["clouds"]["all"],
            "visibility": data.get("visibility", 10000) / 1000,  # meters to km
        }

        # Add rain/snow information if present
        if "rain" in data:
            weather_info["rain"] = data["rain"].get("1h", 0)
        if "snow" in data:
            weather_info["snow"] = data["snow"].get("1h", 0)

        return weather_info

    except requests.exceptions.RequestException as e:
        return {"error": f"Erreur lors de la récupération de la météo: {str(e)}"}
    except KeyError as e:
        return {"error": f"Erreur de parsing des données météo: {str(e)}"}


def get_forecast(city: str, country_code: Optional[str] = None, days: int = 5) -> Dict[str, Any]:
    """
    Get weather forecast for a city (up to 5 days).

    Args:
        city: City name
        country_code: Optional 2-letter country code
        days: Number of days to forecast (1-5)

    Returns:
        Dictionary with forecast information by day
    """
    if not OPENWEATHER_API_KEY:
        return {"error": "OPENWEATHER_API_KEY not configured"}

    location = f"{city},{country_code}" if country_code else city

    try:
        response = requests.get(
            f"{BASE_URL}/forecast",
            params={
                "q": location,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric",
                "lang": "fr"
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        # Group forecasts by day
        forecasts_by_day = {}

        for item in data["list"][:days*8]:  # 8 forecasts per day (every 3 hours)
            dt = datetime.fromtimestamp(item["dt"])
            date_key = dt.date().isoformat()

            if date_key not in forecasts_by_day:
                forecasts_by_day[date_key] = {
                    "date": date_key,
                    "day_name": dt.strftime("%A"),
                    "temperatures": [],
                    "conditions": [],
                    "rain_probability": 0,
                    "wind_speeds": [],
                    "humidity": []
                }

            forecasts_by_day[date_key]["temperatures"].append(item["main"]["temp"])
            forecasts_by_day[date_key]["conditions"].append(item["weather"][0]["main"])
            forecasts_by_day[date_key]["wind_speeds"].append(item["wind"]["speed"] * 3.6)
            forecasts_by_day[date_key]["humidity"].append(item["main"]["humidity"])

            if "rain" in item:
                forecasts_by_day[date_key]["rain_probability"] = max(
                    forecasts_by_day[date_key]["rain_probability"],
                    item.get("pop", 0) * 100
                )

        # Calculate daily summaries
        daily_forecasts = []
        for date_key, day_data in list(forecasts_by_day.items())[:days]:
            temps = day_data["temperatures"]
            daily_forecasts.append({
                "date": day_data["date"],
                "day_name": day_data["day_name"],
                "temperature": {
                    "min": round(min(temps), 1),
                    "max": round(max(temps), 1),
                    "avg": round(sum(temps) / len(temps), 1)
                },
                "dominant_condition": max(set(day_data["conditions"]), key=day_data["conditions"].count),
                "rain_probability": round(day_data["rain_probability"], 0),
                "avg_wind_speed": round(sum(day_data["wind_speeds"]) / len(day_data["wind_speeds"]), 1),
                "avg_humidity": round(sum(day_data["humidity"]) / len(day_data["humidity"]), 0)
            })

        return {
            "city": data["city"]["name"],
            "country": data["city"]["country"],
            "forecasts": daily_forecasts
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Erreur lors de la récupération des prévisions: {str(e)}"}
    except (KeyError, ValueError) as e:
        return {"error": f"Erreur de parsing des prévisions: {str(e)}"}


def get_weather_summary(city: str, country_code: Optional[str] = None) -> str:
    """
    Get a human-readable weather summary.

    Args:
        city: City name
        country_code: Optional 2-letter country code

    Returns:
        Formatted string with weather information
    """
    weather = get_current_weather(city, country_code)

    if "error" in weather:
        return f"❌ {weather['error']}"

    temp = weather["temperature"]["current"]
    feels = weather["temperature"]["feels_like"]
    conditions = weather["conditions"]["description"]
    wind = weather["wind_speed"]
    humidity = weather["humidity"]

    summary = f"""🌤️ Météo actuelle à {weather['city']}, {weather['country']}:

🌡️ Température: {temp}°C (ressenti {feels}°C)
☁️ Conditions: {conditions}
💨 Vent: {wind} km/h
💧 Humidité: {humidity}%
"""

    if "rain" in weather:
        summary += f"🌧️ Pluie: {weather['rain']} mm/h\n"

    return summary.strip()
