# 🌤️ Meteo Outfit Advisor Agent

Un agent intelligent qui recommande les vêtements appropriés en fonction de la météo de votre ville.

---

## 🎯 Vue d'ensemble

**Meteo Outfit Advisor** est un agent conversationnel basé sur Google ADK qui vous aide à choisir vos vêtements en fonction:
- 🌡️ De la température actuelle et ressentie
- ☁️ Des conditions météorologiques (pluie, vent, neige, etc.)
- 💼 De l'occasion (travail, casual, sport, formel)
- 📅 Des prévisions pour les prochains jours

### Fonctionnalités principales

- 💬 **Interface conversationnelle en français**
- 🌍 **Météo pour n'importe quelle ville dans le monde**
- 👔 **Recommandations détaillées par couches** (haut, bas, chaussures, accessoires)
- 📊 **Prévisions sur plusieurs jours** (jusqu'à 5 jours)
- 🎨 **Suggestions de couleurs** basées sur la météo
- 💡 **Conseils pratiques** (parapluie, hydratation, etc.)

---

## 🏗️ Architecture

```
meteo-agent/
├── agent.py                    # Agent ADK principal
├── main.py                     # Point d'entrée pour tests locaux
├── tools/
│   ├── weather_api.py          # Outils d'API météo (OpenWeatherMap)
│   └── outfit_advisor.py       # Logique de recommandation vestimentaire
├── deploy_agent_engine.py      # Script de déploiement sur Agent Engine
├── test_agent_engine.py        # Script de test pour agent déployé
├── requirements.txt            # Dépendances Python
├── .env                        # Variables d'environnement (local)
└── README.md                   # Ce fichier
```

---

## 🚀 Installation

### 1. Prérequis

- Python 3.9+
- Compte Google Cloud (pour déploiement)
- Clé API Gemini (https://aistudio.google.com/apikey)
- Clé API OpenWeatherMap (https://openweathermap.org/api - gratuit)

### 2. Installation des dépendances

```bash
cd /Users/antoinelefetz/Projets/meteo-agent

# Créer un environnement virtuel (recommandé)
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer .env et ajouter vos clés API
# GOOGLE_API_KEY=votre_clé_gemini
# OPENWEATHER_API_KEY=votre_clé_openweather
```

---

## 🧪 Test en Local

### Test rapide

```bash
python main.py
```

### Test avec une question spécifique

```bash
python main.py "Quels vêtements pour aujourd'hui à Paris?"
python main.py "Je vais au travail à Lyon, qu'est-ce que je mets?"
python main.py "Météo pour les 5 prochains jours à Marseille"
```

---

## 📱 Utilisation

### Exemples de questions

#### Pour aujourd'hui:
```
• "Quels vêtements pour aujourd'hui à Paris?"
• "Qu'est-ce que je mets pour sortir à Lyon?"
• "Comment m'habiller aujourd'hui à Marseille?"
```

#### Pour une occasion spécifique:
```
• "Je vais au travail à Nice, qu'est-ce que je mets?"
• "Quel outfit pour faire du sport à Bordeaux?"
• "Je vais à un événement formel à Toulouse, comment m'habiller?"
```

#### Pour les prochains jours:
```
• "Météo pour les 3 prochains jours à Strasbourg"
• "Prévisions pour la semaine à Lille"
• "Qu'est-ce que je dois prévoir pour ce weekend à Nantes?"
```

---

## 🌐 Déploiement sur Agent Engine

### Déploiement complet

```bash
# 1. S'authentifier avec GCP
gcloud auth login
gcloud auth application-default login

# 2. Configurer le projet
export GOOGLE_CLOUD_PROJECT="lil-onboard-gcp"
gcloud config set project $GOOGLE_CLOUD_PROJECT

# 3. Activer les APIs
gcloud services enable aiplatform.googleapis.com storage.googleapis.com

# 4. Déployer l'agent
python deploy_agent_engine.py
```

### Test de l'agent déployé

```bash
# Mode interactif (recommandé)
python test_agent_engine.py --resource-id RESOURCE_ID --interactive

# Test avec une question
python test_agent_engine.py --resource-id RESOURCE_ID \
    --query "Quels vêtements pour aujourd'hui à Paris?"
```

---

## 🛠️ Comment ça marche

### 1. Récupération de la météo

L'agent utilise l'API OpenWeatherMap pour obtenir:
- Température actuelle et ressentie
- Conditions météo (clair, nuageux, pluie, etc.)
- Humidité, vent, visibilité
- Prévisions jusqu'à 5 jours

### 2. Analyse des conditions

Le système analyse:
- **Température**: Catégorisation (très froid, froid, frais, doux, chaud, très chaud)
- **Précipitations**: Pluie, neige, risque
- **Vent**: Force et impact sur le ressenti
- **Humidité**: Confort et respirabilité

### 3. Recommandations vestimentaires

Basé sur l'analyse, l'agent recommande:

#### Couches de vêtements:
- **Très froid (< 0°C)**: Sous-vêtements thermiques, pull épais, doudoune, écharpe, bonnet
- **Froid (0-10°C)**: T-shirt, pull, veste mi-saison
- **Frais (10-15°C)**: T-shirt, cardigan, veste légère
- **Doux (15-20°C)**: T-shirt, chemise légère
- **Chaud (20-25°C)**: T-shirt, polo, chemise manches courtes
- **Très chaud (> 25°C)**: Vêtements légers, lin, débardeur

#### Bas:
- Pantalon épais, jean, chino, short (selon température)

#### Chaussures:
- Bottes fourrées, bottines, baskets, sandales (selon température et météo)

#### Accessoires:
- Parapluie, imperméable (si pluie)
- Écharpe, gants, bonnet (si froid)
- Lunettes de soleil, chapeau (si chaud)

### 4. Adaptation selon l'occasion

- **Casual**: Vêtements décontractés et confortables
- **Travail**: Tenue professionnelle (chemise, pantalon de costume)
- **Sport**: Vêtements techniques respirants
- **Formel**: Costume complet, cravate

---

## 🎨 Outils Disponibles

L'agent dispose de 2 outils principaux:

### 1. `get_weather_and_outfit`
Obtient la météo actuelle et recommande un outfit complet.

**Paramètres:**
- `city`: Nom de la ville
- `country_code`: Code pays optionnel (FR, US, etc.)
- `occasion`: Type d'occasion (casual, work, sport, formal)

**Exemple:**
```python
get_weather_and_outfit(city="Paris", country_code="FR", occasion="work")
```

### 2. `get_forecast_with_advice`
Obtient les prévisions météo avec conseils pour plusieurs jours.

**Paramètres:**
- `city`: Nom de la ville
- `country_code`: Code pays optionnel
- `days`: Nombre de jours (1-5)

**Exemple:**
```python
get_forecast_with_advice(city="Lyon", country_code="FR", days=3)
```

---

## 📊 Format des Réponses

### Météo actuelle + Outfit

```
🌤️ Météo actuelle à Paris, FR:

🌡️ Température: 15°C (ressenti 13°C)
☁️ Conditions: nuageux
💨 Vent: 12 km/h
💧 Humidité: 70%

👔 Recommandations Vestimentaires
==================================================

📊 Catégorie de température: Frais (10-15°C)

🧥 Haut du corps:
   • T-shirt ou chemise
   • Pull léger ou cardigan
   • Veste légère (optionnel)

👖 Bas du corps:
   • Jean
   • Pantalon
   • Chino

👞 Chaussures:
   • Baskets
   • Chaussures de ville

💡 Conseils:
   🌡️ Température fraîche, prévoyez une couche supplémentaire.
```

### Prévisions

```
📅 Prévisions météo pour Marseille, FR (3 jours)

==================================================
📆 Lundi (2025-11-05)
🌡️ Températures: 12°C - 18°C (moy: 15°C)
☁️ Conditions: Clear
🌧️ Probabilité de pluie: 10%
💨 Vent moyen: 15 km/h

💡 👔 Vêtements de mi-saison recommandés

[... autres jours ...]
```

---

## 🔧 Configuration Avancée

### Variables d'environnement (.env)

```bash
# API Keys (requis)
GOOGLE_API_KEY=your_gemini_api_key
OPENWEATHER_API_KEY=your_openweather_api_key

# Configuration par défaut
DEFAULT_CITY=Paris
DEFAULT_COUNTRY_CODE=FR

# Configuration GCP (pour déploiement)
GOOGLE_CLOUD_PROJECT=lil-onboard-gcp
AGENT_ENGINE_REGION=europe-west1
```

### Personnalisation de l'agent

Vous pouvez modifier les recommandations dans `tools/outfit_advisor.py`:
- Seuils de température
- Types de vêtements recommandés
- Conseils et accessoires
- Couleurs suggérées

---

## 🐛 Dépannage

### "API key not configured"

```bash
# Vérifier que .env existe et contient les clés
cat .env

# Si .env n'existe pas
cp .env.example .env
# Puis éditer .env avec vos clés
```

### "Permission denied" (déploiement)

```bash
# S'authentifier à nouveau
gcloud auth application-default login
```

### "City not found"

- Vérifier l'orthographe de la ville
- Essayer avec le code pays (ex: "Paris,FR")
- Utiliser le nom anglais pour certaines villes

---

## 💰 Coûts Estimés

### APIs Gratuites
- **OpenWeatherMap**: 1000 appels/jour gratuits
- **Gemini API**: Usage quotidien généreux

### Agent Engine (si déployé)
- **Développement**: ~5-10€/mois
- **Production légère**: ~20-50€/mois
- Facturation à l'usage (temps de calcul + tokens)

---

## 🚦 Roadmap / Améliorations Futures

- [ ] Support de plusieurs langues (anglais, espagnol, etc.)
- [ ] Préférences utilisateur personnalisées
- [ ] Intégration avec calendrier (événements à venir)
- [ ] Photos d'exemples d'outfits
- [ ] Historique des recommandations
- [ ] Alertes météo personnalisées
- [ ] Intégration avec garde-robe virtuelle

---

## 📝 Exemples d'Usage

### Scenario 1: Préparation pour le travail

```
User: "Je vais au travail à Lyon demain, qu'est-ce que je mets?"

Agent:
🌤️ Météo actuelle à Lyon, FR:
🌡️ Température: 8°C (ressenti 6°C)
☁️ Conditions: légèrement nuageux
💨 Vent: 8 km/h
💧 Humidité: 65%

👔 Recommandations Vestimentaires (Travail)
🧥 Haut: Chemise + Pull + Veste de costume
👖 Bas: Pantalon de costume ou Chino élégant
👞 Chaussures: Chaussures de ville, Derbies, Richelieu
💡 Il fait frais! Prévoyez une couche supplémentaire.
👔 Tenue professionnelle recommandée.
```

### Scenario 2: Weekend sportif

```
User: "Quel outfit pour faire du sport à Nice samedi?"

Agent:
[Météo pour Nice samedi]
👔 Recommandations Vestimentaires (Sport)
🧥 Haut: T-shirt technique + Veste de sport
👖 Bas: Short de sport ou Legging de sport
👞 Chaussures: Chaussures de running, Baskets de sport
🎒 Accessoires: Bouteille d'eau
💡 Vêtements techniques respirants recommandés.
🏃 Pensez à vous hydrater!
```

---

## 🤝 Contribution

Ce projet est développé pour SFEIR.

Pour signaler un bug ou suggérer une amélioration:
1. Créer une issue avec description détaillée
2. Inclure des exemples de requêtes problématiques
3. Fournir des logs si possible

---

## 📄 Licence

Projet interne SFEIR.

---

## 🔗 Liens Utiles

- **ADK Documentation**: https://google.github.io/adk-docs/
- **OpenWeatherMap API**: https://openweathermap.org/api
- **Vertex AI Agent Engine**: https://cloud.google.com/vertex-ai/docs/agent-engine
- **SFEIR**: https://sfeir.com
- **SFEIR Institute**: https://institute.sfeir.com

---

**Développé avec ❤️ pour SFEIR**
