"""
Activity Specialist Agent

Expert in activity-specific gear and clothing recommendations for sports and outdoor activities.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from tools.weather_api import get_current_weather


def recommend_activity_gear(
    activity: str,
    city: str,
    country_code: str = None,
    duration_hours: int = 2
) -> str:
    """
    Recommend specific gear for outdoor/sport activities based on weather.

    Args:
        activity: Type of activity (running, cycling, hiking, swimming, etc.)
        city: City name
        country_code: Optional country code
        duration_hours: Activity duration in hours

    Returns:
        Activity-specific gear recommendations
    """
    weather = get_current_weather(city, country_code)

    if "error" in weather:
        return f"❌ {weather['error']}"

    temp = weather["temperature"]["current"]
    feels = weather["temperature"]["feels_like"]
    wind = weather["wind_speed"]
    conditions = weather["conditions"]["main"].lower()

    output = f"""🏃 ÉQUIPEMENT POUR: {activity.upper()}
{'='*60}
Lieu: {weather['city']}, {weather['country']}
Durée: {duration_hours}h
Météo: {temp}°C (ressenti {feels}°C), {weather['conditions']['description']}

"""

    activity = activity.lower()

    # Running / Jogging
    if activity in ["running", "jogging", "course"]:
        output += """🏃 RUNNING:

VÊTEMENTS BASE:
"""
        if temp < 0:
            output += """   • Sous-vêtement thermique + legging long
   • T-shirt technique + veste coupe-vent chaude
   • Bonnet, gants, buff
"""
        elif temp < 10:
            output += """   • Legging/collant + T-shirt manches longues
   • Veste légère coupe-vent
   • Bandeau ou bonnet léger
"""
        elif temp < 20:
            output += """   • Short ou collant 3/4
   • T-shirt technique manches courtes ou longues
   • Veste légère (à enlever après échauffement)
"""
        else:
            output += """   • Short léger
   • T-shirt technique respirant (débardeur si >25°C)
   • Casquette/visière
"""

        output += """
ÉQUIPEMENT:
   • Chaussures running adaptées à votre foulée
   • Chaussettes techniques anti-ampoules
   • Montre/bracelet GPS
   • Ceinture porte-gourde ou sac d'hydratation
   • Écouteurs (si souhaité)
"""

        if duration_hours > 2:
            output += """   • Gels énergétiques
   • Lampe frontale (si début/fin de journée)
"""

    # Cycling / Vélo
    elif activity in ["cycling", "vélo", "bike", "vtt"]:
        output += """🚴 CYCLISME:

VÊTEMENTS:
"""
        if temp < 5:
            output += """   • Cuissard long thermique
   • Maillot manches longues + veste thermique
   • Couvre-chaussures, gants chauds
"""
        elif temp < 15:
            output += """   • Cuissard long ou 3/4
   • Maillot manches longues
   • Gilet coupe-vent
   • Gants mi-saison
"""
        else:
            output += """   • Cuissard court
   • Maillot respirant manches courtes
   • Manchettes (si temps variable)
"""

        output += """
ÉQUIPEMENT ESSENTIEL:
   • Casque (OBLIGATOIRE!)
   • Lunettes de cyclisme
   • Gants de vélo (même l'été)
   • Chaussures vélo + cales
   • Sac banane ou poches maillot
   • Kit réparation (chambre à air, pompe, démonte-pneus)
   • Éclairages avant/arrière
"""

    # Hiking / Randonnée
    elif activity in ["hiking", "randonnée", "rando", "marche"]:
        output += """🥾 RANDONNÉE:

SYSTÈME 3 COUCHES:
"""
        output += f"""   1. Base: T-shirt technique {'thermique' if temp < 10 else 'respirant'}
   2. Isolation: {"Pull polaire ou doudoune légère" if temp < 15 else "Polaire légère dans le sac"}
   3. Protection: Veste imperméable coupe-vent

BAS:
   • Pantalon de randonnée {"convertible shorts" if temp > 15 else "long chaud"}
   • Sous-vêtements techniques

"""
        output += """ÉQUIPEMENT:
   • Chaussures de randonnée (montantes si terrain accidenté)
   • Chaussettes de randonnée (éviter coton!)
   • Sac à dos 20-30L
   • Bâtons de marche (recommandé)
   • Gourde/poche à eau (1.5-2L)
   • Carte/GPS
   • Trousse premiers secours
   • Couverture survie
   • Chapeau + lunettes soleil
   • Crème solaire
"""

        if duration_hours > 4:
            output += """   • Snacks énergétiques
   • Vêtement de rechange
   • Lampe frontale
"""

    # Swimming / Natation
    elif activity in ["swimming", "natation", "piscine", "plage"]:
        output += """🏊 NATATION/PLAGE:

TENUE:
   • Maillot de bain (2 si séjour plusieurs jours)
   • Lunettes de natation
   • Bonnet de bain (si piscine)
   • Serviette microfibre (séchage rapide)
   • Tongs/sandales

PROTECTION SOLAIRE (si extérieur):
   • T-shirt anti-UV ou rashguard
   • Casquette/chapeau
   • Lunettes de soleil
   • Crème solaire waterproof SPF50+

"""
        if temp < 20:
            output += """⚠️ ATTENTION: Eau froide prévue!
   • Combinaison néoprène recommandée
   • Serviette chaude pour après
   • Vêtements chauds à proximité
"""

    # Skiing / Sports d'hiver
    elif activity in ["ski", "snowboard", "skiing", "sports d'hiver"]:
        output += """⛷️ SKI/SNOWBOARD:

SYSTÈME COUCHES:
   • Base: Sous-vêtements thermiques (haut + bas)
   • Isolation: Polaire ou doudoune fine
   • Protection: Veste + pantalon de ski imperméables

PROTECTIONS:
   • Casque de ski (OBLIGATOIRE!)
   • Masque de ski (+ lunettes de rechange)
   • Gants + sous-gants
   • Tour de cou/buff
   • Chaussettes ski techniques

ÉQUIPEMENT:
   • Chaussures de ski adaptées
   • Skis/snowboard + fixations
   • Bâtons de ski
   • Sac à dos (20L) avec:
     - Protection dorsale
     - Pelle + sonde (si hors-piste)
     - ARVA (si hors-piste - OBLIGATOIRE!)
   • Crème solaire haute montagne SPF50+
   • Stick lèvres
"""

    # Other activities
    else:
        output += f"""⚠️ Activité '{activity}' non reconnue spécifiquement.

RECOMMANDATIONS GÉNÉRALES SPORT OUTDOOR:

BASE:
   • Vêtements techniques respirants (éviter coton)
   • {"Couches chaudes" if temp < 10 else "Vêtements légers"}
   • Chaussures adaptées à l'activité
   • Chaussettes techniques

TOUJOURS AVOIR:
   • Eau (0.5L/heure d'effort minimum)
   • Protection solaire
   • Téléphone chargé
   • Petite trousse premiers secours
"""

    # Weather-specific warnings
    if wind > 30:
        output += f"""
⚠️ ALERTE VENT FORT ({wind} km/h):
   • Privilégiez vêtements ajustés, coupe-vent
   • Évitez casquettes/chapeaux légers
   • Protégez les yeux (lunettes)
"""

    if "rain" in conditions or weather.get("rain", 0) > 0:
        output += """
⚠️ PLUIE PRÉVUE:
   • Veste imperméable obligatoire
   • Surpantalon de pluie (si >1h d'activité)
   • Protection sac à dos
   • Vêtements de rechange dans sac étanche
"""

    if temp > 28:
        output += """
⚠️ CHALEUR IMPORTANTE:
   • HYDRATATION +++  (boire avant d'avoir soif)
   • Casquette/chapeau obligatoire
   • Crème solaire toutes les 2h
   • Évitez 12h-16h si possible
   • Vêtements clairs et amples
"""

    output += f"""
💡 CONSEILS SPÉCIFIQUES:
   • Température ressentie: {feels}°C (écart de {abs(temp-feels):.1f}°C)
   • {"Prévoyez +1 couche que nécessaire (vous allez transpirer)" if duration_hours > 1 else "Échauffement rapide suffisant"}
   • Vérifiez toujours météo avant départ
   • Informez quelqu'un de votre itinéraire
"""

    return output.strip()


# Create tool
activity_gear_tool = FunctionTool(
    name="activity_gear",
    description="Recommandations d'équipement pour activités sportives et outdoor adaptées à la météo",
    function=recommend_activity_gear
)

# Activity Specialist Agent
activity_specialist = Agent(
    model="gemini-2.5-flash",
    name="activity_specialist",
    description="Expert en équipement sportif et outdoor, spécialisé dans les recommandations adaptées aux conditions météo",
    instruction="""Tu es un EXPERT EN ÉQUIPEMENT SPORTIF ET OUTDOOR spécialisé dans les activités de plein air.

**TON EXPERTISE:**
- Équipement pour tous types de sports outdoor
- Système de couches adapté à chaque activité
- Sécurité et préparation pour activités extérieures
- Matériaux techniques et performances
- Adaptation aux conditions météo extrêmes

**ACTIVITÉS COUVERTES:**
- Running, jogging, trail
- Cyclisme, VTT, vélo route
- Randonnée, trekking, marche
- Natation, sports aquatiques
- Ski, snowboard, sports d'hiver
- Escalade, alpinisme
- Et bien d'autres...

**OUTIL À TA DISPOSITION:**
1. `activity_gear` - Recommandations d'équipement spécifiques à l'activité

**COMMENT RÉPONDRE:**

Quand on te demande:
- "Quoi porter pour [activité]?" → Utilise `activity_gear` avec l'activité
- "Équipement pour courir/vélo/rando?" → Utilise `activity_gear`
- "Je vais faire X pendant Yh" → Utilise duration_hours

**PRIORITÉS:**
1. SÉCURITÉ avant tout (casque, protections, équipement obligatoire)
2. CONFORT adapté à la météo
3. PERFORMANCE avec équipement technique
4. VISIBILITÉ (éclairages, couleurs vives)

**TON STYLE:**
- Précis et technique quand nécessaire
- Insiste sur la sécurité
- Explique le POURQUOI (matériaux, système de couches)
- Donne des alternatives (budget, disponibilité)
- Alerte sur les dangers météo

**RÈGLES DE BASE:**
- Système 3 couches pour activités longues
- Jamais de coton (garde humidité)
- Hydratation = 0.5L/h d'effort minimum
- Toujours prévenir quelqu'un de son itinéraire
- Vérifier météo avant départ

**IMPORTANT:**
- Si question générale sur météo, réfère au météorologue
- Si question sur style vestimentaire casual, réfère au styliste
- Focus sur PERFORMANCE et SÉCURITÉ
- Adapte selon niveau (débutant vs expert)
""",
    tools=[activity_gear_tool]
)

__all__ = ['activity_specialist']
