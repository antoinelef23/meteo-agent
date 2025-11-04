# Meteo Outfit Advisor - Project Summary

✅ **Project successfully created!**

---

## 🎯 What Is This?

A smart AI agent that recommends what to wear based on the weather in your city. Built with Google ADK and ready to deploy on Vertex AI Agent Engine.

### Key Features

- 🌤️ **Real-time weather** from OpenWeatherMap API
- 👔 **Smart outfit recommendations** based on temperature, conditions, and occasion
- 📅 **Multi-day forecasts** (up to 5 days)
- 💼 **Occasion-aware** (casual, work, sport, formal)
- 🇫🇷 **French interface**
- 🚀 **Ready for Agent Engine** deployment

---

## 📁 Project Structure

```
meteo-agent/
├── 📄 agent.py                      Main ADK agent with tools
├── 📄 main.py                       Local testing entry point
├── 📁 tools/
│   ├── __init__.py                  Package initialization
│   ├── weather_api.py               Weather data from OpenWeatherMap
│   └── outfit_advisor.py            Outfit recommendation logic
├── 📄 deploy_agent_engine.py        Deploy to Vertex AI Agent Engine
├── 📄 test_agent_engine.py          Test deployed agent
├── 📄 requirements.txt              Python dependencies
├── 📄 .env.example                  Environment variables template
├── 📄 .gitignore                    Git ignore file
├── 📄 README.md                     Complete documentation
├── 📄 QUICKSTART.md                 5-minute quick start guide
└── 📄 PROJECT_SUMMARY.md            This file
```

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Google ADK** | Agent framework |
| **Gemini 2.5 Flash** | LLM model |
| **OpenWeatherMap API** | Weather data |
| **Vertex AI Agent Engine** | Production hosting |
| **Python 3.9+** | Programming language |

---

## 🚀 How to Use

### 1. Quick Local Test (30 seconds)

```bash
cd /Users/antoinelefetz/Projets/meteo-agent

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Install dependencies
pip install -r requirements.txt

# Test!
python main.py "Quels vêtements pour aujourd'hui à Paris?"
```

### 2. Deploy to Agent Engine (5 minutes)

```bash
# Authenticate
gcloud auth login
gcloud auth application-default login

# Set project
export GOOGLE_CLOUD_PROJECT="lil-onboard-gcp"
gcloud config set project $GOOGLE_CLOUD_PROJECT

# Enable APIs
gcloud services enable aiplatform.googleapis.com storage.googleapis.com

# Deploy
python deploy_agent_engine.py
```

### 3. Test Deployed Agent

```bash
# Interactive mode
python test_agent_engine.py --resource-id RESOURCE_ID --interactive
```

---

## 💬 Example Queries

The agent understands natural language questions like:

### Current Weather + Outfit
- "Quels vêtements pour aujourd'hui à Paris?"
- "Qu'est-ce que je mets à Lyon?"
- "Comment m'habiller à Marseille aujourd'hui?"

### Occasion-Specific
- "Je vais au travail à Nice, qu'est-ce que je mets?"
- "Quel outfit pour faire du sport à Bordeaux?"
- "Je vais à un événement formel à Toulouse, comment m'habiller?"

### Forecasts
- "Météo pour les 3 prochains jours à Strasbourg"
- "Prévisions pour la semaine à Lille"
- "Qu'est-ce que je dois prévoir pour ce weekend à Nantes?"

---

## 🧰 Agent Tools

The agent has 2 main tools:

### 1. `get_weather_and_outfit`
Gets current weather and recommends a complete outfit.

**Parameters:**
- `city`: City name (required)
- `country_code`: 2-letter country code (optional)
- `occasion`: "casual", "work", "sport", or "formal" (optional)

### 2. `get_forecast_with_advice`
Gets multi-day weather forecast with outfit suggestions.

**Parameters:**
- `city`: City name (required)
- `country_code`: 2-letter country code (optional)
- `days`: Number of days 1-5 (optional, default 3)

---

## 🧠 Recommendation Logic

The agent analyzes:

### Temperature Ranges
- **< 0°C**: Very cold (thermal underwear, heavy coat, hat, gloves)
- **0-10°C**: Cold (t-shirt, sweater, jacket, scarf)
- **10-15°C**: Cool (t-shirt, cardigan, light jacket)
- **15-20°C**: Mild (t-shirt, light shirt)
- **20-25°C**: Warm (t-shirt, polo, short sleeves)
- **> 25°C**: Hot (light clothing, linen, tank top)

### Weather Conditions
- **Rain**: Add umbrella, raincoat, waterproof shoes
- **Wind**: Recommend fitted clothing, avoid light hats
- **Snow**: Add boots, hat, gloves
- **High humidity**: Recommend breathable fabrics

### Occasions
- **Casual**: Comfortable, relaxed clothing
- **Work**: Professional attire (shirt, dress pants, dress shoes)
- **Sport**: Technical, breathable athletic wear
- **Formal**: Full suit, tie, polished dress shoes

---

## 📊 Response Format

### Current Weather + Outfit Example

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

---

## 🔐 Required API Keys

### 1. Google Gemini API
- **Get it**: https://aistudio.google.com/apikey
- **Cost**: Free tier available
- **Purpose**: Powers the AI agent

### 2. OpenWeatherMap API
- **Get it**: https://openweathermap.org/api
- **Cost**: 1000 calls/day free
- **Purpose**: Weather data

Add both to `.env` file:
```bash
GOOGLE_API_KEY=your_gemini_key_here
OPENWEATHER_API_KEY=your_openweather_key_here
```

---

## 💰 Cost Estimates

### Development/Testing
- **OpenWeatherMap**: Free (1000 calls/day)
- **Gemini API**: Free tier
- **Agent Engine**: ~5-10€/month

### Light Production
- **OpenWeatherMap**: Free or ~10€/month for more calls
- **Gemini API**: Usage-based (~20-30€/month)
- **Agent Engine**: ~30-50€/month

**Total**: ~40-90€/month for light production use

---

## 🎨 Customization

### Change Temperature Thresholds
Edit `tools/outfit_advisor.py`:
```python
def recommend_outfit(weather_data, occasion="casual"):
    # Modify temperature ranges
    if feels_like < 0:
        # Very cold recommendations
    elif feels_like < 10:
        # Cold recommendations
    # ... etc
```

### Add New Occasions
Add new function in `tools/outfit_advisor.py`:
```python
def _adjust_for_beach(recommendations, temp):
    """Beach outfit recommendations"""
    recommendations["layers"] = ["Maillot de bain", "T-shirt léger"]
    # ... etc
```

### Change Default City
Edit `.env`:
```bash
DEFAULT_CITY=Lyon
DEFAULT_COUNTRY_CODE=FR
```

---

## 🔄 Workflow

```
User Query
    ↓
Agent receives question
    ↓
Agent identifies tool to use
    ↓
get_weather_and_outfit OR get_forecast_with_advice
    ↓
weather_api.py → OpenWeatherMap API
    ↓
outfit_advisor.py → Analyzes conditions
    ↓
Generates recommendations
    ↓
Agent formats response
    ↓
User receives outfit advice
```

---

## 📚 Documentation

| File | Description |
|------|-------------|
| `README.md` | Complete documentation (20+ pages) |
| `QUICKSTART.md` | 5-minute quick start guide |
| `PROJECT_SUMMARY.md` | This file - project overview |

---

## 🐛 Troubleshooting

### "API key not configured"
→ Check `.env` file exists and contains both API keys

### "Permission denied" (deployment)
→ Run `gcloud auth application-default login`

### "City not found"
→ Try with country code: "Paris,FR"

### Import errors
→ Run `pip install -r requirements.txt`

---

## ✅ Testing Checklist

Before deploying to production:

- [ ] Test local agent with `python main.py`
- [ ] Test with different cities
- [ ] Test different occasions (casual, work, sport, formal)
- [ ] Test multi-day forecasts
- [ ] Verify API keys work
- [ ] Deploy to Agent Engine
- [ ] Test deployed agent with `test_agent_engine.py`
- [ ] Try edge cases (extreme temperatures, bad weather)

---

## 🚦 Next Steps

### Immediate (now)

1. Get API keys:
   - Gemini: https://aistudio.google.com/apikey
   - OpenWeatherMap: https://openweathermap.org/api

2. Configure `.env`:
   ```bash
   cp .env.example .env
   # Edit .env with your keys
   ```

3. Test locally:
   ```bash
   pip install -r requirements.txt
   python main.py
   ```

### Short-term (when GCP project is ready)

4. Deploy to Agent Engine:
   ```bash
   python deploy_agent_engine.py
   ```

5. Test deployed agent:
   ```bash
   python test_agent_engine.py --resource-id ID --interactive
   ```

### Long-term (enhancements)

- [ ] Add user preferences persistence
- [ ] Integrate with calendar
- [ ] Add outfit images/examples
- [ ] Multi-language support
- [ ] Weather alerts
- [ ] Virtual wardrobe integration

---

## 📞 Support

- **ADK Documentation**: https://google.github.io/adk-docs/
- **OpenWeatherMap Docs**: https://openweathermap.org/api
- **Agent Engine Docs**: https://cloud.google.com/vertex-ai/docs/agent-engine

---

## 🎉 Summary

You now have a complete, production-ready AI agent that:

✅ Provides real-time weather data
✅ Recommends appropriate outfits
✅ Adapts to different occasions
✅ Supports multiple cities worldwide
✅ Works in French
✅ Can be deployed to Agent Engine in minutes
✅ Is fully documented

**Ready to help you never dress wrong for the weather again!** 🌤️👔

---

**Developed for SFEIR**
*[sfeir.com](https://sfeir.com) | [institute.sfeir.com](https://institute.sfeir.com)*

*Created: 2025-11-04*
