"""
Outfit recommendation logic based on weather conditions
"""

from typing import Dict, List, Any


def recommend_outfit(weather_data: Dict[str, Any], occasion: str = "casual") -> Dict[str, Any]:
    """
    Recommend outfit based on weather conditions.

    Args:
        weather_data: Weather information from weather_api
        occasion: Type of occasion (casual, work, sport, formal)

    Returns:
        Dictionary with outfit recommendations
    """
    if "error" in weather_data:
        return {"error": weather_data["error"]}

    temp = weather_data["temperature"]["current"]
    feels_like = weather_data["temperature"]["feels_like"]
    conditions = weather_data["conditions"]["main"].lower()
    wind_speed = weather_data["wind_speed"]
    humidity = weather_data["humidity"]
    has_rain = weather_data.get("rain", 0) > 0

    # Base recommendations
    recommendations = {
        "temperature_category": _get_temp_category(feels_like),
        "layers": [],
        "bottoms": [],
        "shoes": [],
        "accessories": [],
        "tips": [],
        "colors_mood": []
    }

    # Temperature-based clothing
    if feels_like < 0:
        # Very cold (< 0°C)
        recommendations["layers"] = [
            "Sous-vêtements thermiques",
            "Pull ou sweat épais",
            "Manteau d'hiver / Doudoune",
            "Écharpe",
            "Bonnet"
        ]
        recommendations["bottoms"] = ["Pantalon épais", "Jean doublé"]
        recommendations["shoes"] = ["Bottes fourrées", "Chaussures montantes"]
        recommendations["accessories"].extend(["Gants chauds", "Écharpe épaisse"])
        recommendations["tips"].append("⚠️ Il fait très froid ! Couvrez-vous bien.")

    elif feels_like < 10:
        # Cold (0-10°C)
        recommendations["layers"] = [
            "T-shirt ou chemise",
            "Pull ou gilet",
            "Veste / Manteau mi-saison"
        ]
        recommendations["bottoms"] = ["Jean", "Pantalon", "Chino"]
        recommendations["shoes"] = ["Baskets", "Bottines", "Chaussures fermées"]
        recommendations["accessories"].append("Écharpe légère (optionnel)")
        recommendations["tips"].append("🧥 Pensez à une veste, il fait frais.")

    elif feels_like < 15:
        # Cool (10-15°C)
        recommendations["layers"] = [
            "T-shirt ou chemise",
            "Pull léger ou cardigan",
            "Veste légère (optionnel)"
        ]
        recommendations["bottoms"] = ["Jean", "Pantalon", "Chino"]
        recommendations["shoes"] = ["Baskets", "Chaussures de ville"]
        recommendations["tips"].append("🌡️ Température fraîche, prévoyez une couche supplémentaire.")

    elif feels_like < 20:
        # Mild (15-20°C)
        recommendations["layers"] = [
            "T-shirt",
            "Chemise légère",
            "Pull léger (à porter sur les épaules)"
        ]
        recommendations["bottoms"] = ["Jean", "Chino", "Pantalon léger"]
        recommendations["shoes"] = ["Baskets", "Chaussures de ville", "Mocassins"]
        recommendations["tips"].append("😊 Température agréable !")

    elif feels_like < 25:
        # Warm (20-25°C)
        recommendations["layers"] = [
            "T-shirt",
            "Chemise à manches courtes",
            "Polo"
        ]
        recommendations["bottoms"] = ["Jean", "Chino", "Short (si décontracté)"]
        recommendations["shoes"] = ["Baskets", "Sandales fermées", "Mocassins"]
        recommendations["tips"].append("☀️ Temps agréable et doux.")

    else:
        # Hot (> 25°C)
        recommendations["layers"] = [
            "T-shirt léger",
            "Chemise en lin",
            "Débardeur (si très chaud)"
        ]
        recommendations["bottoms"] = ["Short", "Pantalon léger", "Bermuda"]
        recommendations["shoes"] = ["Sandales", "Baskets légères", "Tongs (plage)"]
        recommendations["accessories"].extend(["Chapeau", "Lunettes de soleil"])
        recommendations["tips"].append("🌞 Il fait chaud ! Restez léger et hydraté.")

    # Weather condition adjustments
    if conditions in ["rain", "drizzle", "thunderstorm"] or has_rain:
        recommendations["accessories"].extend(["Parapluie", "Imperméable ou veste de pluie"])
        recommendations["shoes"] = ["Bottes de pluie", "Chaussures imperméables"]
        recommendations["tips"].append("🌧️ Pluie prévue, prenez un parapluie !")

    if wind_speed > 30:
        recommendations["tips"].append(f"💨 Vent fort ({wind_speed} km/h), privilégiez des vêtements ajustés.")
        recommendations["accessories"].append("Évitez les chapeaux légers")

    if conditions == "snow":
        recommendations["accessories"].append("Bonnet et gants")
        recommendations["shoes"] = ["Bottes de neige", "Chaussures imperméables"]
        recommendations["tips"].append("❄️ Neige prévue, équipez-vous !")

    if humidity > 80 and temp > 20:
        recommendations["tips"].append("💧 Humidité élevée, privilégiez des tissus respirants.")

    # Occasion-based adjustments
    if occasion.lower() == "work":
        recommendations = _adjust_for_work(recommendations, temp)
    elif occasion.lower() == "sport":
        recommendations = _adjust_for_sport(recommendations, temp)
    elif occasion.lower() == "formal":
        recommendations = _adjust_for_formal(recommendations, temp)

    # Color and mood suggestions
    if conditions in ["clear", "sun"]:
        recommendations["colors_mood"] = ["Couleurs vives", "Blanc", "Pastels"]
    elif conditions in ["clouds", "mist", "fog"]:
        recommendations["colors_mood"] = ["Couleurs neutres", "Gris", "Beige", "Noir"]
    elif conditions in ["rain", "drizzle"]:
        recommendations["colors_mood"] = ["Couleurs sombres", "Bleu marine", "Noir"]

    return recommendations


def _get_temp_category(temp: float) -> str:
    """Get temperature category as a string"""
    if temp < 0:
        return "Très froid (< 0°C)"
    elif temp < 10:
        return "Froid (0-10°C)"
    elif temp < 15:
        return "Frais (10-15°C)"
    elif temp < 20:
        return "Doux (15-20°C)"
    elif temp < 25:
        return "Chaud (20-25°C)"
    else:
        return "Très chaud (> 25°C)"


def _adjust_for_work(recommendations: Dict, temp: float) -> Dict:
    """Adjust recommendations for work/professional context"""
    # More formal clothing
    recommendations["layers"] = [
        "Chemise" if temp > 15 else "Chemise + Pull",
        "Veste de costume (optionnel)" if temp > 20 else "Veste de costume"
    ]
    recommendations["bottoms"] = ["Pantalon de costume", "Chino élégant"]
    recommendations["shoes"] = ["Chaussures de ville", "Derbies", "Richelieu"]
    recommendations["tips"].append("👔 Tenue professionnelle recommandée.")
    return recommendations


def _adjust_for_sport(recommendations: Dict, temp: float) -> Dict:
    """Adjust recommendations for sport/athletic activities"""
    recommendations["layers"] = [
        "T-shirt technique" if temp > 15 else "T-shirt technique + Veste de sport",
        "Legging ou short de sport"
    ]
    recommendations["bottoms"] = ["Short de sport", "Legging de sport", "Pantalon de jogging"]
    recommendations["shoes"] = ["Chaussures de running", "Baskets de sport"]
    recommendations["accessories"] = ["Bouteille d'eau", "Bandeau (si chaud)"]
    recommendations["tips"].append("🏃 Vêtements techniques respirants recommandés.")
    return recommendations


def _adjust_for_formal(recommendations: Dict, temp: float) -> Dict:
    """Adjust recommendations for formal events"""
    recommendations["layers"] = [
        "Chemise habillée",
        "Costume complet",
        "Cravate ou nœud papillon"
    ]
    recommendations["bottoms"] = ["Pantalon de costume"]
    recommendations["shoes"] = ["Chaussures de ville cirées", "Richelieu"]
    recommendations["accessories"] = ["Ceinture assortie", "Pochette (optionnel)"]
    recommendations["tips"].append("🎩 Tenue formelle de rigueur.")
    return recommendations


def format_outfit_recommendation(recommendations: Dict[str, Any]) -> str:
    """
    Format outfit recommendations as a readable string.

    Args:
        recommendations: Dictionary from recommend_outfit()

    Returns:
        Formatted string with outfit advice
    """
    if "error" in recommendations:
        return f"❌ {recommendations['error']}"

    output = f"""👔 Recommandations Vestimentaires
{'='*50}

📊 Catégorie de température: {recommendations['temperature_category']}

"""

    if recommendations["layers"]:
        output += "🧥 Haut du corps:\n"
        for item in recommendations["layers"]:
            output += f"   • {item}\n"
        output += "\n"

    if recommendations["bottoms"]:
        output += "👖 Bas du corps:\n"
        for item in recommendations["bottoms"]:
            output += f"   • {item}\n"
        output += "\n"

    if recommendations["shoes"]:
        output += "👞 Chaussures:\n"
        for item in recommendations["shoes"]:
            output += f"   • {item}\n"
        output += "\n"

    if recommendations["accessories"]:
        output += "🎒 Accessoires:\n"
        for item in recommendations["accessories"]:
            output += f"   • {item}\n"
        output += "\n"

    if recommendations["colors_mood"]:
        output += "🎨 Palette de couleurs suggérée:\n"
        output += f"   {', '.join(recommendations['colors_mood'])}\n\n"

    if recommendations["tips"]:
        output += "💡 Conseils:\n"
        for tip in recommendations["tips"]:
            output += f"   {tip}\n"

    return output.strip()
