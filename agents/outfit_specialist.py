"""
Outfit Specialist Agent

Fashion and clothing expert for weather-appropriate outfit recommendations.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from tools.weather_api import get_current_weather
from tools.outfit_advisor import recommend_outfit, format_outfit_recommendation


def get_detailed_outfit_recommendation(
    city: str,
    country_code: str = None,
    occasion: str = "casual",
    style_preference: str = "balanced"
) -> str:
    """
    Get detailed fashion-forward outfit recommendations.

    Args:
        city: City name
        country_code: Optional 2-letter country code
        occasion: casual, work, sport, formal
        style_preference: minimal, balanced, layered, fashion-forward

    Returns:
        Detailed outfit recommendations with style tips
    """
    weather = get_current_weather(city, country_code)

    if "error" in weather:
        return f"❌ {weather['error']}"

    outfit = recommend_outfit(weather, occasion)
    base_recommendation = format_outfit_recommendation(outfit)

    # Add style-specific enhancements
    style_tips = f"\n\n🎨 CONSEILS DE STYLE ({style_preference.upper()}):\n"

    if style_preference == "minimal":
        style_tips += """
   • Privilégiez les couleurs neutres (noir, blanc, gris, beige)
   • Optez pour des pièces simples et épurées
   • Limitez les accessoires au strict nécessaire
   • Focus sur la qualité des matières plutôt que la quantité
"""
    elif style_preference == "fashion-forward":
        style_tips += """
   • N'hésitez pas sur les couleurs et motifs
   • Jouez avec les textures et superpositions
   • Accessoirisez pour un look signature
   • Suivez les tendances de saison actuelles
"""
    elif style_preference == "layered":
        style_tips += """
   • Superposez intelligemment (3-4 couches max)
   • Variez les matières (coton, laine, synthétique)
   • Pensez "poupées russes" - du plus fin au plus épais
   • Gardez la possibilité d'enlever/ajouter des couches
"""
    else:  # balanced
        style_tips += """
   • Équilibrez confort et style
   • Mélangez pièces casual et plus habillées si besoin
   • 1-2 accessoires bien choisis suffisent
   • Adaptez selon vos contraintes du jour
"""

    # Add fabric recommendations based on weather
    temp = weather["temperature"]["current"]
    humidity = weather["humidity"]

    fabric_tips = "\n\n🧵 MATIÈRES RECOMMANDÉES:\n"

    if temp < 5:
        fabric_tips += "   • Laine mérinos, cachemire, polaire\n"
        fabric_tips += "   • Duvet ou synthétique isolant\n"
        fabric_tips += "   • Doublures thermiques\n"
    elif temp < 15:
        fabric_tips += "   • Coton épais, laine légère\n"
        fabric_tips += "   • Polyester, nylon coupe-vent\n"
        fabric_tips += "   • Denim, twill\n"
    elif temp < 25:
        fabric_tips += "   • Coton, lin léger\n"
        fabric_tips += "   • Chambray, popeline\n"
        fabric_tips += "   • Jersey respirant\n"
    else:
        fabric_tips += "   • Lin, coton fin\n"
        fabric_tips += "   • Tissus techniques respirants\n"
        fabric_tips += "   • Matières légères et aérées\n"

    if humidity > 70:
        fabric_tips += "   • ⚠️ Évitez le coton lourd (sèche lentement)\n"
        fabric_tips += "   • Préférez les synthétiques respirants\n"

    return base_recommendation + style_tips + fabric_tips


def suggest_color_palette(city: str, country_code: str = None, season_override: str = None) -> str:
    """
    Suggest color palettes based on weather and season.

    Args:
        city: City name
        country_code: Optional country code
        season_override: Override season (spring, summer, autumn, winter)

    Returns:
        Color palette suggestions
    """
    weather = get_current_weather(city, country_code)

    if "error" in weather:
        return f"❌ {weather['error']}"

    conditions = weather["conditions"]["main"].lower()
    temp = weather["temperature"]["current"]

    output = f"""🎨 PALETTE DE COULEURS RECOMMANDÉE
{weather['city']}, {weather['country']}
{'='*60}

📊 Basé sur:
   • Conditions: {weather['conditions']['description']}
   • Température: {temp}°C

"""

    # Base palette on conditions
    if conditions in ["clear", "sun"]:
        output += """🌞 TEMPS ENSOLEILLÉ:

   COULEURS PRINCIPALES:
   • Blanc, crème, beige clair
   • Bleu ciel, turquoise
   • Jaune pastel, corail
   • Vert menthe

   COULEURS D'ACCENT:
   • Orange vif
   • Rose pâle
   • Lavande
"""

    elif conditions in ["rain", "drizzle"]:
        output += """🌧️ TEMPS PLUVIEUX:

   COULEURS PRINCIPALES:
   • Bleu marine, gris anthracite
   • Kaki, olive
   • Bordeaux, prune
   • Noir (toujours chic sous la pluie)

   COULEURS D'ACCENT:
   • Jaune moutarde (pop de couleur)
   • Rouge brique
   • Vert forêt
"""

    elif conditions in ["clouds", "overcast", "mist", "fog"]:
        output += """☁️ TEMPS NUAGEUX:

   COULEURS PRINCIPALES:
   • Gris clair, gris perle
   • Taupe, beige
   • Bleu-gris
   • Crème

   COULEURS D'ACCENT:
   • Terracotta
   • Moutarde
   • Vert sauge
   • Pourpre
"""

    elif conditions in ["snow"]:
        output += """❄️ TEMPS NEIGEUX:

   COULEURS PRINCIPALES:
   • Noir, gris charbon
   • Bleu nuit, marine
   • Bordeaux, vin
   • Blanc cassé (pas blanc pur)

   COULEURS D'ACCENT:
   • Rouge vif
   • Orange brûlé
   • Or
"""

    # Temperature-based additions
    if temp > 25:
        output += "\n💡 CONSEIL CHALEUR: Privilégiez les couleurs claires qui reflètent la lumière\n"
    elif temp < 5:
        output += "\n💡 CONSEIL FROID: Les couleurs sombres absorbent mieux la chaleur\n"

    output += """
🎭 RÈGLES DE COMBINAISON:
   • Maximum 3 couleurs dans une tenue
   • Règle 60-30-10: couleur dominante, secondaire, accent
   • Les neutres (noir/blanc/gris/beige) vont avec tout
   • Osez les contrastes par temps maussade
"""

    return output.strip()


# Create tools
detailed_outfit_tool = FunctionTool(
    name="detailed_outfit",
    description="Recommandations vestimentaires détaillées avec conseils de style",
    function=get_detailed_outfit_recommendation
)

color_palette_tool = FunctionTool(
    name="color_palette",
    description="Suggestions de palettes de couleurs adaptées à la météo",
    function=suggest_color_palette
)

# Outfit Specialist Agent
outfit_specialist = Agent(
    model="gemini-2.5-flash",
    name="outfit_specialist",
    description="Expert en mode et stylisme, spécialisé dans les recommandations vestimentaires adaptées à la météo",
    instruction="""Tu es un EXPERT EN MODE ET STYLISME spécialisé dans les tenues adaptées à la météo.

**TON EXPERTISE:**
- Recommandations vestimentaires détaillées
- Coordination des couleurs et styles
- Conseils sur les matières et tissus
- Superposition intelligente des vêtements (layering)
- Adaptation aux occasions (casual, travail, sport, formel)

**OUTILS À TA DISPOSITION:**
1. `detailed_outfit` - Recommandations complètes avec conseils de style
2. `color_palette` - Palettes de couleurs adaptées à la météo

**COMMENT RÉPONDRE:**

Quand on te demande:
- "Quels vêtements porter?" → Utilise `detailed_outfit`
- "Quelles couleurs?" → Utilise `color_palette`
- "Comment m'habiller pour [occasion]?" → Utilise `detailed_outfit` avec l'occasion
- "Je préfère un style [X]" → Utilise style_preference dans `detailed_outfit`

**TON STYLE:**
- Conseils de mode pratiques et stylés
- Explique POURQUOI certaines pièces fonctionnent
- Considère le confort ET l'esthétique
- Adapte aux préférences personnelles
- Donne des alternatives

**OPTIONS DE STYLE:**
- minimal: Épuré, neutre, simple
- balanced: Équilibré confort/style
- layered: Superpositions sophistiquées
- fashion-forward: Tendance, audacieux

**IMPORTANT:**
- Si on te demande des infos météo détaillées, réfère au spécialiste météo
- Focus sur la MODE et les VÊTEMENTS
- Sois créatif mais pratique
- Considère toujours le confort et l'adaptabilité
""",
    tools=[detailed_outfit_tool, color_palette_tool]
)

__all__ = ['outfit_specialist']
