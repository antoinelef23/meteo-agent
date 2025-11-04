"""
Weather Specialist Agent

Expert in weather analysis, forecasts, and meteorological patterns.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from tools.weather_api import get_current_weather, get_forecast, get_weather_summary

# Weather specialist tools
def analyze_weather_conditions(city: str, country_code: str = None) -> str:
    """
    Provide detailed weather analysis and meteorological insights.

    Args:
        city: City name
        country_code: Optional 2-letter country code

    Returns:
        Detailed weather analysis
    """
    weather = get_current_weather(city, country_code)

    if "error" in weather:
        return f"❌ {weather['error']}"

    temp = weather["temperature"]["current"]
    feels = weather["temperature"]["feels_like"]
    conditions = weather["conditions"]["description"]
    wind = weather["wind_speed"]
    humidity = weather["humidity"]

    analysis = f"""🌤️ ANALYSE MÉTÉO DÉTAILLÉE - {weather['city']}, {weather['country']}
{'='*60}

📊 TEMPÉRATURES:
   • Actuelle: {temp}°C
   • Ressentie: {feels}°C (écart de {abs(temp - feels):.1f}°C)
   • Min/Max du jour: {weather['temperature']['min']}°C / {weather['temperature']['max']}°C

☁️ CONDITIONS ATMOSPHÉRIQUES:
   • État: {conditions}
   • Nébulosité: {weather['clouds']}%
   • Visibilité: {weather['visibility']} km

💨 VENT & HUMIDITÉ:
   • Vitesse du vent: {wind} km/h
   • Humidité relative: {humidity}%

🔬 ANALYSE:
"""

    # Temperature analysis
    if abs(temp - feels) > 3:
        if feels < temp:
            analysis += f"   • Le vent fait que la température ressentie est {abs(temp - feels):.1f}°C plus froide\n"
        else:
            analysis += f"   • L'humidité fait que la température ressentie est {abs(temp - feels):.1f}°C plus chaude\n"

    # Wind analysis
    if wind > 40:
        analysis += "   • ⚠️ Vent très fort - conditions difficiles\n"
    elif wind > 25:
        analysis += "   • Vent modéré à fort - attention aux objets légers\n"
    elif wind > 15:
        analysis += "   • Vent faible à modéré\n"
    else:
        analysis += "   • Vent calme\n"

    # Humidity analysis
    if humidity > 80:
        analysis += "   • Humidité élevée - sensation de lourdeur possible\n"
    elif humidity < 30:
        analysis += "   • Air sec - hydratation importante\n"

    # Rain info
    if "rain" in weather and weather["rain"] > 0:
        analysis += f"   • 🌧️ Pluie active: {weather['rain']} mm/h\n"

    return analysis.strip()


def get_extended_forecast(city: str, country_code: str = None, days: int = 5) -> str:
    """
    Get detailed extended weather forecast with trends.

    Args:
        city: City name
        country_code: Optional 2-letter country code
        days: Number of days (1-5)

    Returns:
        Detailed forecast with analysis
    """
    forecast = get_forecast(city, country_code, days)

    if "error" in forecast:
        return f"❌ {forecast['error']}"

    output = f"""📅 PRÉVISIONS MÉTÉO DÉTAILLÉES
{forecast['city']}, {forecast['country']} - {days} jours
{'='*60}

"""

    temps = []
    for i, day in enumerate(forecast["forecasts"]):
        output += f"""
📆 {day['day_name'].upper()} ({day['date']})
{'-'*60}
🌡️ Températures:
   • Min: {day['temperature']['min']}°C
   • Max: {day['temperature']['max']}°C
   • Moyenne: {day['temperature']['avg']}°C

☁️ Conditions: {day['dominant_condition']}
🌧️ Probabilité de pluie: {day['rain_probability']}%
💨 Vent moyen: {day['avg_wind_speed']} km/h
💧 Humidité moyenne: {day['avg_humidity']}%
"""
        temps.append(day['temperature']['avg'])

    # Trend analysis
    output += f"\n{'='*60}\n📈 ANALYSE DES TENDANCES:\n"

    if len(temps) >= 2:
        if temps[-1] > temps[0] + 3:
            output += "   • 📈 Tendance au réchauffement sur la période\n"
        elif temps[-1] < temps[0] - 3:
            output += "   • 📉 Tendance au refroidissement sur la période\n"
        else:
            output += "   • ➡️ Températures stables sur la période\n"

    avg_temp = sum(temps) / len(temps)
    output += f"   • Température moyenne de la période: {avg_temp:.1f}°C\n"

    # Rain analysis
    rainy_days = sum(1 for day in forecast["forecasts"] if day['rain_probability'] > 50)
    if rainy_days > 0:
        output += f"   • 🌧️ {rainy_days} jour(s) avec forte probabilité de pluie\n"

    return output.strip()


# Create tools
analyze_weather_tool = FunctionTool(
    name="analyze_weather",
    description="Analyse météorologique détaillée des conditions actuelles",
    function=analyze_weather_conditions
)

extended_forecast_tool = FunctionTool(
    name="extended_forecast",
    description="Prévisions météo détaillées avec analyse des tendances",
    function=get_extended_forecast
)

# Weather Specialist Agent
weather_specialist = Agent(
    model="gemini-2.5-flash",
    name="weather_specialist",
    description="Expert météorologue spécialisé dans l'analyse détaillée des conditions climatiques et des prévisions",
    instruction="""Tu es un MÉTÉOROLOGUE EXPERT spécialisé dans l'analyse approfondie des conditions météorologiques.

**TON EXPERTISE:**
- Analyse détaillée des conditions atmosphériques
- Interprétation des données météorologiques
- Prévisions et tendances climatiques
- Impact du vent, de l'humidité, de la pression
- Phénomènes météorologiques

**OUTILS À TA DISPOSITION:**
1. `analyze_weather` - Analyse détaillée des conditions actuelles
2. `extended_forecast` - Prévisions sur plusieurs jours avec tendances

**COMMENT RÉPONDRE:**

Quand on te demande:
- "Quelle est la météo?" → Utilise `analyze_weather` pour une analyse complète
- "Prévisions pour X jours" → Utilise `extended_forecast`
- "Va-t-il pleuvoir?" → Analyse les prévisions et probabilités
- "Quel temps fait-il?" → Analyse détaillée des conditions actuelles

**TON STYLE:**
- Précis et technique quand nécessaire
- Explique les phénomènes météorologiques
- Mentionne les impacts concrets (ressenti, visibilité, etc.)
- Donne des tendances et prévisions

**IMPORTANT:**
- Reste concentré sur la MÉTÉO uniquement
- Si on te demande des conseils vestimentaires, indique que ton collègue spécialiste des tenues peut aider
- Fournis des données factuelles et analyses météorologiques
- Explique les phénomènes (pourquoi le vent refroidit, impact de l'humidité, etc.)
""",
    tools=[analyze_weather_tool, extended_forecast_tool]
)

__all__ = ['weather_specialist']
