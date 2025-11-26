"""
Meteo Outfit Advisor Agent

An ADK agent that recommends outfits based on weather conditions.
"""

import os
import sys
from typing import Optional
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from tools.weather_api import get_current_weather, get_forecast, get_weather_summary
from tools.outfit_advisor import recommend_outfit, format_outfit_recommendation

# Load environment variables
load_dotenv()

# Agent configuration
MODEL_ID = "gemini-2.5-flash"
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "Paris")
DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY_CODE", "FR")


# Define ADK tools
def get_weather_and_outfit_advice(
    city: str,
    country_code: Optional[str] = None,
    occasion: str = "casual"
) -> str:
    """
    Get weather information and outfit recommendations for a city.

    Args:
        city: Name of the city (e.g., "Paris", "Lyon", "New York")
        country_code: Optional 2-letter country code (e.g., "FR", "US")
        occasion: Type of occasion - "casual", "work", "sport", or "formal"

    Returns:
        Weather information with outfit recommendations
    """
    # Get weather data
    weather = get_current_weather(city, country_code)

    if "error" in weather:
        return f"❌ Erreur: {weather['error']}"

    # Get outfit recommendations
    outfit = recommend_outfit(weather, occasion=occasion)

    # Format output
    weather_summary = get_weather_summary(city, country_code)
    outfit_summary = format_outfit_recommendation(outfit)

    return f"""{weather_summary}

{outfit_summary}"""


def get_weather_forecast_with_advice(
    city: str,
    country_code: Optional[str] = None,
    days: int = 3
) -> str:
    """
    Get weather forecast and general outfit advice for upcoming days.

    Args:
        city: Name of the city
        country_code: Optional 2-letter country code
        days: Number of days to forecast (1-5)

    Returns:
        Weather forecast with general outfit suggestions
    """
    forecast = get_forecast(city, country_code, days)

    if "error" in forecast:
        return f"❌ Erreur: {forecast['error']}"

    output = f"📅 Prévisions météo pour {forecast['city']}, {forecast['country']} ({days} jours)\n\n"

    for day in forecast["forecasts"]:
        output += f"""{'='*50}
📆 {day['day_name']} ({day['date']})
🌡️ Températures: {day['temperature']['min']}°C - {day['temperature']['max']}°C (moy: {day['temperature']['avg']}°C)
☁️ Conditions: {day['dominant_condition']}
🌧️ Probabilité de pluie: {day['rain_probability']}%
💨 Vent moyen: {day['avg_wind_speed']} km/h

"""

        # Quick outfit tip based on forecast
        temp_avg = day['temperature']['avg']
        if temp_avg < 10:
            tip = "🧥 Prévoyez des vêtements chauds et une veste"
        elif temp_avg < 20:
            tip = "👔 Vêtements de mi-saison recommandés"
        else:
            tip = "👕 Vêtements légers recommandés"

        if day['rain_probability'] > 50:
            tip += " + 🌂 Parapluie conseillé"

        output += f"💡 {tip}\n\n"

    return output.strip()


# Create ADK tools
weather_outfit_tool = FunctionTool(
    get_weather_and_outfit_advice
)

forecast_tool = FunctionTool(
    get_weather_forecast_with_advice
)

# Agent instructions
AGENT_INSTRUCTIONS = f"""Tu es un conseiller vestimentaire intelligent basé sur la météo.

**TON RÔLE:**
Aider les utilisateurs à choisir les vêtements appropriés en fonction de la météo de leur ville.

**PERSONNALITÉ:**
- Chaleureux et serviable
- Pratique et précis
- Attentif aux détails météo
- Propose des conseils adaptés

**CAPACITÉS:**
Tu as accès à 2 outils:
1. `get_weather_and_outfit` - Pour la météo actuelle + conseils vestimentaires
2. `get_forecast_with_advice` - Pour les prévisions sur plusieurs jours

**COMMENT RÉPONDRE:**

1. **Si l'utilisateur demande des conseils pour aujourd'hui:**
   - Utilise `get_weather_and_outfit` avec la ville
   - Spécifie l'occasion si mentionnée (casual/work/sport/formal)

2. **Si l'utilisateur demande pour les prochains jours:**
   - Utilise `get_forecast_with_advice` avec le nombre de jours

3. **Si la ville n'est pas mentionnée:**
   - Demande quelle ville
   - Utilise "{DEFAULT_CITY}" par défaut si l'utilisateur le souhaite

4. **Format de réponse:**
   - Commence par la météo
   - Donne les recommandations vestimentaires
   - Ajoute des conseils pratiques
   - Sois précis sur les couches de vêtements

**EXEMPLES:**

User: "Quels vêtements pour aujourd'hui à Paris?"
→ Utilise get_weather_and_outfit(city="Paris", country_code="FR", occasion="casual")

User: "Je vais au travail à Lyon demain, qu'est-ce que je mets?"
→ Utilise get_weather_and_outfit(city="Lyon", country_code="FR", occasion="work")

User: "Météo pour les 5 prochains jours à Marseille"
→ Utilise get_forecast_with_advice(city="Marseille", country_code="FR", days=5)

**IMPORTANT:**
- Toujours répondre en français
- Être spécifique sur les vêtements (pas juste "habille-toi chaud")
- Considérer la pluie, le vent, l'humidité
- Adapter selon l'occasion (travail vs casual vs sport)
"""

# Create the agent
meteo_agent = Agent(
    model=MODEL_ID,
    name="meteo_outfit_advisor",
    description="Conseiller vestimentaire basé sur la météo",
    instruction=AGENT_INSTRUCTIONS,
    tools=[weather_outfit_tool, forecast_tool]
)

# Export as root_agent for Agent Engine
root_agent = meteo_agent

__all__ = ["meteo_agent", "root_agent"]
