"""
Weather API tools for fetching weather data from WeatherAPI.com
"""

import os
import requests
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY")
BASE_URL = "http://api.weatherapi.com/v1"


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
    if not WEATHERAPI_KEY:
        return {"error": "WEATHERAPI_KEY not configured"}

    # Build location query
    location = f"{city},{country_code}" if country_code else city

    try:
        # Call WeatherAPI.com API
        response = requests.get(
            f"{BASE_URL}/current.json",
            params={
                "q": location,
                "key": WEATHERAPI_KEY,
                "lang": "fr"  # French descriptions
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        # Parse and structure the response
        weather_info = {
            "city": data["location"]["name"],
            "country": data["location"]["country"],
            "timestamp": data["location"]["localtime"],
            "temperature": {
                "current": round(data["current"]["temp_c"], 1),
                "feels_like": round(data["current"]["feelslike_c"], 1),
                "min": round(data["current"]["temp_c"], 1),  # WeatherAPI doesn't provide min/max in current
                "max": round(data["current"]["temp_c"], 1)
            },
            "conditions": {
                "main": data["current"]["condition"]["text"],
                "description": data["current"]["condition"]["text"],
                "icon": data["current"]["condition"]["icon"]
            },
            "humidity": data["current"]["humidity"],
            "wind_speed": round(data["current"]["wind_kph"], 1),
            "clouds": data["current"]["cloud"],
            "visibility": round(data["current"]["vis_km"], 1),
        }

        # Add rain/snow information if present
        if data["current"]["precip_mm"] > 0:
            weather_info["rain"] = data["current"]["precip_mm"]

        return weather_info

    except requests.exceptions.RequestException as e:
        return {"error": f"Erreur lors de la récupération de la météo: {str(e)}"}
    except KeyError as e:
        return {"error": f"Erreur de parsing des données météo: {str(e)}"}


def get_forecast(city: str, country_code: Optional[str] = None, days: int = 5) -> Dict[str, Any]:
    """
    Get weather forecast for a city (up to 14 days with WeatherAPI.com).

    Args:
        city: City name
        country_code: Optional 2-letter country code
        days: Number of days to forecast (1-14)

    Returns:
        Dictionary with forecast information by day
    """
    if not WEATHERAPI_KEY:
        return {"error": "WEATHERAPI_KEY not configured"}

    location = f"{city},{country_code}" if country_code else city

    # Limit to 14 days max for WeatherAPI
    days = min(days, 14)

    try:
        response = requests.get(
            f"{BASE_URL}/forecast.json",
            params={
                "q": location,
                "key": WEATHERAPI_KEY,
                "days": days,
                "lang": "fr"
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        # Parse daily forecasts
        daily_forecasts = []

        for day in data["forecast"]["forecastday"]:
            # Parse date
            forecast_date = datetime.strptime(day["date"], "%Y-%m-%d")

            daily_forecasts.append({
                "date": day["date"],
                "day_name": forecast_date.strftime("%A"),
                "temperature": {
                    "min": round(day["day"]["mintemp_c"], 1),
                    "max": round(day["day"]["maxtemp_c"], 1),
                    "avg": round(day["day"]["avgtemp_c"], 1)
                },
                "dominant_condition": day["day"]["condition"]["text"],
                "rain_probability": round(day["day"]["daily_chance_of_rain"], 0),
                "avg_wind_speed": round(day["day"]["maxwind_kph"], 1),
                "avg_humidity": round(day["day"]["avghumidity"], 0)
            })

        return {
            "city": data["location"]["name"],
            "country": data["location"]["country"],
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
