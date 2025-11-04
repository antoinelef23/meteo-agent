"""
Travel Planner Agent

Expert in trip planning, packing lists, and multi-destination outfit coordination.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from tools.weather_api import get_forecast
from tools.outfit_advisor import recommend_outfit


def generate_packing_list(
    city: str,
    country_code: str = None,
    days: int = 3,
    trip_type: str = "leisure"
) -> str:
    """
    Generate smart packing list based on weather forecast.

    Args:
        city: Destination city
        country_code: Optional country code
        days: Trip duration (1-5 days)
        trip_type: leisure, business, adventure, beach

    Returns:
        Detailed packing list
    """
    forecast = get_forecast(city, country_code, min(days, 5))

    if "error" in forecast:
        return f"❌ {forecast['error']}"

    output = f"""🧳 LISTE DE VALISE INTELLIGENTE
{'='*60}
Destination: {forecast['city']}, {forecast['country']}
Durée: {days} jours
Type de voyage: {trip_type.upper()}

"""

    # Analyze temperature range across all days
    all_temps = []
    rain_days = 0
    for day in forecast["forecasts"]:
        all_temps.extend([day["temperature"]["min"], day["temperature"]["max"]])
        if day["rain_probability"] > 50:
            rain_days += 1

    temp_min = min(all_temps)
    temp_max = max(all_temps)
    temp_range = temp_max - temp_min

    output += f"""📊 ANALYSE MÉTÉO DU SÉJOUR:
   • Températures: {temp_min}°C à {temp_max}°C (amplitude: {temp_range}°C)
   • Jours de pluie probables: {rain_days}/{len(forecast['forecasts'])}
   • {'⚠️ Grande amplitude thermique!' if temp_range > 15 else '✅ Températures stables'}

📋 VÊTEMENTS ESSENTIELS:

"""

    # Base items depending on temp range
    items = {}

    # Tops
    if temp_max > 20:
        items["👕 HAUTS"] = [
            f"{days + 1} T-shirts",
            "1-2 chemises légères",
        ]
    if temp_min < 15:
        items["👕 HAUTS"] = items.get("👕 HAUTS", []) + [
            "1-2 pulls légers",
            "1 veste/gilet"
        ]
    if temp_min < 5:
        items["👕 HAUTS"] = items.get("👕 HAUTS", []) + [
            "1 manteau chaud",
            "Pull épais"
        ]

    # Bottoms
    bottoms = []
    if trip_type == "business":
        bottoms = [
            f"{(days // 2) + 1} pantalons de costume",
            "1 jean (casual)"
        ]
    elif trip_type == "beach":
        bottoms = [
            f"{(days // 2) + 1} shorts",
            "1 pantalon léger",
            "2 maillots de bain"
        ]
    else:
        bottoms = [
            f"{(days // 2) + 1} pantalons/jeans",
            "1-2 shorts (si chaud)" if temp_max > 20 else "2-3 pantalons"
        ]
    items["👖 BAS"] = bottoms

    # Shoes
    if trip_type == "adventure":
        items["👞 CHAUSSURES"] = [
            "1 paire chaussures de randonnée",
            "1 paire baskets confortables",
            "1 paire sandales/tongs"
        ]
    elif trip_type == "business":
        items["👞 CHAUSSURES"] = [
            "1 paire chaussures de ville",
            "1 paire baskets/mocassins (déplacements)"
        ]
    else:
        items["👞 CHAUSSURES"] = [
            "1 paire baskets confortables",
            "1 paire chaussures ville/casual",
            "1 paire sandales" if temp_max > 20 else "1 paire bottines"
        ]

    # Accessories based on weather
    accessories = []
    if rain_days > 0:
        accessories.extend(["Parapluie compact", "Veste imperméable"])
    if temp_min < 10:
        accessories.extend(["Écharpe", "Bonnet", "Gants" if temp_min < 5 else ""])
    if temp_max > 25:
        accessories.extend(["Chapeau/casquette", "Lunettes de soleil"])

    items["🎒 ACCESSOIRES"] = [a for a in accessories if a]

    # Print items
    for category, item_list in items.items():
        output += f"\n{category}:\n"
        for item in item_list:
            output += f"   ☐ {item}\n"

    # Essential items
    output += f"""
💼 ESSENTIELS (toujours):
   ☐ Sous-vêtements ({days + 1})
   ☐ Chaussettes ({days + 1})
   ☐ Pyjama/vêtements de nuit
   ☐ Trousse de toilette
   ☐ Chargeurs (téléphone, etc.)
"""

    if trip_type == "business":
        output += """   ☐ Tenue formelle complète
   ☐ Cravate/accessoires pro
   ☐ Ordinateur + accessoires
"""

    # Pro tips
    output += f"""
💡 ASTUCES DE PRO:
   • Roulez les vêtements (gain de place 30%)
   • Portez les pièces les plus volumineuses en voyage
   • 1 tenue = 1 sac de compression
   • Couleurs neutres = plus de combinaisons possibles
"""

    if temp_range > 10:
        output += "   • ⚠️ Grande variété de températures: prévoyez des couches modulables!\n"

    if rain_days > days / 2:
        output += "   • 🌧️ Pluie fréquente: privilégiez les matières à séchage rapide\n"

    return output.strip()


def plan_daily_outfits(
    city: str,
    country_code: str = None,
    days: int = 3,
    occasions: str = "casual"
) -> str:
    """
    Plan daily outfit for each day of trip.

    Args:
        city: Destination city
        country_code: Country code
        days: Number of days
        occasions: Comma-separated occasions per day (e.g., "casual,work,casual")

    Returns:
        Daily outfit plan
    """
    forecast = get_forecast(city, country_code, min(days, 5))

    if "error" in forecast:
        return f"❌ {forecast['error']}"

    # Parse occasions
    occasion_list = [o.strip() for o in occasions.split(",")]
    if len(occasion_list) < days:
        occasion_list.extend(["casual"] * (days - len(occasion_list)))

    output = f"""📅 PLANNING TENUES - VOYAGE À {forecast['city']}
{'='*60}

"""

    for i, day in enumerate(forecast["forecasts"][:days]):
        occasion = occasion_list[i] if i < len(occasion_list) else "casual"

        output += f"""
{'='*60}
JOUR {i+1} - {day['day_name']} ({day['date']})
{'='*60}

🌡️ Météo: {day['temperature']['min']}°C - {day['temperature']['max']}°C
☁️ Conditions: {day['dominant_condition']}
🌧️ Pluie: {day['rain_probability']}%
💼 Occasion: {occasion.upper()}

👔 TENUE RECOMMANDÉE:
"""

        # Get weather data in the right format
        weather_data = {
            "temperature": {
                "current": day['temperature']['avg'],
                "feels_like": day['temperature']['avg'],
                "min": day['temperature']['min'],
                "max": day['temperature']['max']
            },
            "conditions": {
                "main": day['dominant_condition'],
                "description": day['dominant_condition']
            },
            "wind_speed": day['avg_wind_speed'],
            "humidity": day['avg_humidity'],
            "clouds": 50
        }

        if day['rain_probability'] > 50:
            weather_data["rain"] = 1

        outfit = recommend_outfit(weather_data, occasion)

        # Format outfit suggestions
        if outfit.get("layers"):
            output += "   Haut: " + ", ".join(outfit["layers"][:2]) + "\n"
        if outfit.get("bottoms"):
            output += "   Bas: " + outfit["bottoms"][0] + "\n"
        if outfit.get("shoes"):
            output += "   Chaussures: " + outfit["shoes"][0] + "\n"
        if outfit.get("accessories"):
            output += "   Accessoires: " + ", ".join(outfit["accessories"][:2]) + "\n"

        if outfit.get("tips"):
            output += f"\n   💡 {outfit['tips'][0]}\n"

    return output.strip()


# Create tools
packing_list_tool = FunctionTool(
    name="packing_list",
    description="Générer une liste de valise intelligente basée sur la météo prévue",
    function=generate_packing_list
)

daily_outfits_tool = FunctionTool(
    name="daily_outfits",
    description="Planifier les tenues jour par jour pour un voyage",
    function=plan_daily_outfits
)

# Travel Planner Agent
travel_planner = Agent(
    model="gemini-2.5-flash",
    name="travel_planner",
    description="Expert en planification de voyages et organisation de valises adaptées à la météo",
    instruction="""Tu es un EXPERT EN PLANIFICATION DE VOYAGES spécialisé dans l'organisation optimale des bagages.

**TON EXPERTISE:**
- Listes de valise intelligentes
- Planning de tenues par jour
- Optimisation de l'espace bagage
- Adaptation aux différents types de voyage (loisir, affaires, aventure)
- Conseils pour voyager léger et efficace

**OUTILS À TA DISPOSITION:**
1. `packing_list` - Générer liste de valise complète
2. `daily_outfits` - Planifier tenues jour par jour

**TYPES DE VOYAGE:**
- leisure: Vacances, détente
- business: Voyage professionnel
- adventure: Randonnée, outdoor, sports
- beach: Plage, mer, soleil

**COMMENT RÉPONDRE:**

Quand on te demande:
- "Que mettre dans ma valise?" → Utilise `packing_list`
- "Préparer mon voyage de X jours" → Utilise `packing_list` avec durée
- "Planning de tenues" → Utilise `daily_outfits`
- "Voyage d'affaires/plage/aventure" → Adapte trip_type

**TON STYLE:**
- Pratique et organisé
- Conseils d'optimisation (roulage, compression)
- Considère les contraintes de poids
- Pense polyvalence (pièces multi-usage)
- Anticipe les imprévus météo

**ASTUCES SIGNATURE:**
- Règle des 3 couches modulables
- Palette de couleurs neutres = max de combos
- 1 paire de chaussures confortables obligatoire
- Articles multi-usage (paréo, écharpe large)
- Toujours une tenue de secours

**IMPORTANT:**
- Adapte aux restrictions de bagages (cabine vs soute)
- Considère les activités spécifiques du voyage
- Si question sur météo seule, réfère au météorologue
- Si question sur style, réfère au styliste
""",
    tools=[packing_list_tool, daily_outfits_tool]
)

__all__ = ['travel_planner']
