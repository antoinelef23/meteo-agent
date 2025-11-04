

# 🤖 Multi-Agent Architecture

## Enhanced Meteo Outfit Advisor with Specialist Agents

The Meteo Outfit Advisor now uses a sophisticated **multi-agent system** with specialized experts for different aspects of weather and clothing recommendations.

---

## 🏗️ Architecture Overview

```
User Query
    ↓
┌─────────────────────────┐
│   COORDINATOR AGENT     │  ← Intelligent Router
│   (decides which        │
│    specialist to use)   │
└─────────────────────────┘
            │
            ├─→ 🌤️  WEATHER SPECIALIST
            │   (meteorology expert)
            │
            ├─→ 👔 OUTFIT SPECIALIST
            │   (fashion & style expert)
            │
            ├─→ ✈️  TRAVEL PLANNER
            │   (packing & trip planning)
            │
            └─→ 🏃 ACTIVITY SPECIALIST
                (sports & outdoor gear)
```

---

## 🤖 The Team of Specialists

### 1. 🎯 Coordinator Agent

**Role**: Intelligent router that analyzes requests and delegates to appropriate specialists.

**Capabilities**:
- Analyzes user intent
- Routes to one or multiple specialists
- Synthesizes responses from multiple agents
- Handles complex multi-aspect queries

**Example Routing**:
```
"Quelle est la météo à Paris?" → Weather Specialist
"Quels vêtements porter?" → Outfit Specialist
"Je pars 3 jours à Nice en vélo" → Travel Planner + Activity Specialist
```

---

### 2. 🌤️ Weather Specialist

**Expertise**: Deep meteorological analysis and forecasting.

**Tools**:
- `analyze_weather` - Detailed weather analysis
- `extended_forecast` - Multi-day forecasts with trends

**What it provides**:
- Detailed atmospheric conditions
- Temperature analysis (actual vs feels-like)
- Wind and humidity impact
- Weather trends and patterns
- Meteorological explanations

**Example Questions**:
```
✅ "Quelle est la météo détaillée à Paris?"
✅ "Va-t-il pleuvoir cette semaine?"
✅ "Pourquoi le vent fait-il plus froid?"
✅ "Analyse météo pour les 5 prochains jours"
```

**Sample Output**:
```
🌤️ ANALYSE MÉTÉO DÉTAILLÉE - Paris, FR
============================================================

📊 TEMPÉRATURES:
   • Actuelle: 15°C
   • Ressentie: 13°C (écart de 2.0°C)
   • Min/Max du jour: 12°C / 18°C

☁️ CONDITIONS ATMOSPHÉRIQUES:
   • État: nuageux
   • Nébulosité: 60%
   • Visibilité: 10 km

💨 VENT & HUMIDITÉ:
   • Vitesse du vent: 15 km/h
   • Humidité relative: 70%

🔬 ANALYSE:
   • Le vent fait que la température ressentie est 2.0°C plus froide
   • Vent faible à modéré
```

---

### 3. 👔 Outfit Specialist

**Expertise**: Fashion, style, and clothing coordination for all occasions.

**Tools**:
- `detailed_outfit` - Complete outfit recommendations with style tips
- `color_palette` - Color scheme suggestions based on weather

**What it provides**:
- Detailed clothing recommendations (layers, bottoms, shoes)
- Style preferences (minimal, balanced, layered, fashion-forward)
- Fabric recommendations
- Color coordination
- Occasion-specific advice (casual, work, sport, formal)

**Style Preferences**:
- **Minimal**: Neutral colors, simple pieces, quality over quantity
- **Balanced**: Comfort + style, practical with flair
- **Layered**: Sophisticated layering, 3-4 layers
- **Fashion-forward**: Bold colors, trendy, statement pieces

**Example Questions**:
```
✅ "Quelles couleurs porter aujourd'hui?"
✅ "Tenue casual pour Paris"
✅ "Style minimaliste pour aller au travail"
✅ "Comment coordonner mes vêtements avec ce temps?"
```

**Sample Output**:
```
👔 RECOMMANDATIONS VESTIMENTAIRES
==================================================

📊 Catégorie de température: Frais (10-15°C)

🧥 Haut du corps:
   • T-shirt ou chemise
   • Pull léger ou cardigan
   • Veste légère (optionnel)

🎨 CONSEILS DE STYLE (MINIMAL):
   • Privilégiez les couleurs neutres (noir, blanc, gris, beige)
   • Optez pour des pièces simples et épurées
   • Limitez les accessoires au strict nécessaire

🧵 MATIÈRES RECOMMANDÉES:
   • Coton épais, laine légère
   • Polyester, nylon coupe-vent
```

---

### 4. ✈️ Travel Planner

**Expertise**: Trip planning, packing optimization, and multi-day outfit coordination.

**Tools**:
- `packing_list` - Smart packing lists based on forecast
- `daily_outfits` - Day-by-day outfit planning

**What it provides**:
- Complete packing lists optimized for weather
- Day-by-day outfit planning
- Trip type adaptation (leisure, business, adventure, beach)
- Packing optimization tips
- Multi-temperature preparation

**Trip Types**:
- **Leisure**: Vacations, relaxation
- **Business**: Professional travel
- **Adventure**: Hiking, outdoor activities
- **Beach**: Coastal, swimming

**Example Questions**:
```
✅ "Je pars 3 jours à Nice, que mettre dans ma valise?"
✅ "Préparer mon voyage d'affaires à Lyon (5 jours)"
✅ "Liste de valise pour un weekend à la plage"
✅ "Planning de tenues pour ma semaine à Paris"
```

**Sample Output**:
```
🧳 LISTE DE VALISE INTELLIGENTE
============================================================
Destination: Nice, FR
Durée: 3 jours
Type de voyage: LEISURE

📊 ANALYSE MÉTÉO DU SÉJOUR:
   • Températures: 18°C à 25°C (amplitude: 7°C)
   • Jours de pluie probables: 0/3
   • ✅ Températures stables

📋 VÊTEMENTS ESSENTIELS:

👕 HAUTS:
   ☐ 4 T-shirts
   ☐ 1-2 chemises légères

👖 BAS:
   ☐ 2 pantalons/jeans
   ☐ 1-2 shorts (si chaud)

👞 CHAUSSURES:
   ☐ 1 paire baskets confortables
   ☐ 1 paire chaussures ville/casual
   ☐ 1 paire sandales

💡 ASTUCES DE PRO:
   • Roulez les vêtements (gain de place 30%)
   • Portez les pièces les plus volumineuses en voyage
```

---

### 5. 🏃 Activity Specialist

**Expertise**: Sports equipment and outdoor gear recommendations.

**Tool**:
- `activity_gear` - Activity-specific equipment lists

**Activities Covered**:
- Running, jogging, trail
- Cycling (road, VTT)
- Hiking, trekking
- Swimming, aquatic sports
- Skiing, snowboarding
- Climbing, mountaineering
- And many more...

**What it provides**:
- Activity-specific gear lists
- Safety equipment (helmets, protections)
- Layering systems for sports
- Technical fabric recommendations
- Weather-specific adjustments
- Duration-based equipment

**Example Questions**:
```
✅ "Équipement pour courir ce matin à Paris"
✅ "Que porter pour faire du vélo (2h) à Lyon?"
✅ "Gear pour une randonnée de 6h à Nice"
✅ "Vêtements de ski pour ce weekend"
```

**Sample Output**:
```
🏃 ÉQUIPEMENT POUR: RUNNING
============================================================
Lieu: Paris, FR
Durée: 2h
Météo: 15°C (ressenti 13°C), nuageux

🏃 RUNNING:

VÊTEMENTS BASE:
   • Legging/collant + T-shirt manches longues
   • Veste légère coupe-vent
   • Bandeau ou bonnet léger

ÉQUIPEMENT:
   • Chaussures running adaptées à votre foulée
   • Chaussettes techniques anti-ampoules
   • Montre/bracelet GPS
   • Ceinture porte-gourde ou sac d'hydratation
   • Gels énergétiques (durée >2h)

💡 CONSEILS SPÉCIFIQUES:
   • Température ressentie: 13°C (écart de 2.0°C)
   • Prévoyez +1 couche que nécessaire (vous allez transpirer)
```

---

## 🔀 How Routing Works

### Simple Queries (1 Specialist)

```
Query: "Quelle est la météo à Paris?"
→ Coordinator analyzes: Weather question
→ Routes to: 🌤️ Weather Specialist
→ User gets: Detailed weather analysis
```

### Complex Queries (Multiple Specialists)

```
Query: "Je pars faire du vélo 3 jours à Nice, aide-moi"
→ Coordinator analyzes: Trip + Activity
→ Routes to: ✈️ Travel Planner (packing list)
           + 🏃 Activity Specialist (cycling gear)
→ User gets: Complete preparation guide
```

### Style-Specific Queries

```
Query: "Tenue casual pour Paris aujourd'hui, style minimal"
→ Coordinator analyzes: Outfit + Style preference
→ Routes to: 👔 Outfit Specialist (with style=minimal)
→ User gets: Minimalist outfit recommendations
```

---

## 💡 Key Advantages of Multi-Agent System

### 1. **Specialized Expertise**
Each agent is an expert in its domain with focused knowledge and tools.

### 2. **Better Responses**
More detailed and accurate responses than a single general agent.

### 3. **Scalability**
Easy to add new specialists (e.g., fashion trends agent, climate change agent).

### 4. **Modularity**
Each agent can be updated independently without affecting others.

### 5. **Complex Query Handling**
Can handle multi-faceted questions by consulting multiple specialists.

### 6. **Clear Responsibilities**
Each agent has a well-defined role, reducing confusion.

---

## 📊 Comparison: Single Agent vs Multi-Agent

| Aspect | Single Agent | Multi-Agent System |
|--------|--------------|-------------------|
| **Expertise** | General knowledge | Deep specialized knowledge |
| **Response Quality** | Good | Excellent |
| **Complex Queries** | Limited | Handles naturally |
| **Maintainability** | Harder to update | Easy (update specific agent) |
| **Scalability** | Limited | Highly scalable |
| **Tool Management** | All tools in one place | Distributed, organized |
| **User Experience** | Simple | Sophisticated, expert-level |

---

## 🎯 Usage Examples

### Example 1: Weather Analysis
```python
Query: "Analyse détaillée de la météo à Paris"

Routing: 🌤️ Weather Specialist

Output:
- Temperature breakdown
- Atmospheric conditions
- Wind and humidity analysis
- Meteorological insights
```

### Example 2: Fashion Advice
```python
Query: "Quelles couleurs porter avec ce temps gris?"

Routing: 👔 Outfit Specialist

Output:
- Weather-appropriate color palette
- Style combinations
- Fabric recommendations
- Mood-based suggestions
```

### Example 3: Trip Planning
```python
Query: "Voyage d'affaires 4 jours à Lyon"

Routing: ✈️ Travel Planner

Output:
- Professional packing list
- Day-by-day outfit planning
- Business-appropriate clothing
- Packing optimization tips
```

### Example 4: Sports Gear
```python
Query: "Équipement pour courir 1h ce matin à Nice"

Routing: 🏃 Activity Specialist

Output:
- Running-specific gear
- Weather-adapted clothing
- Safety equipment
- Duration-specific items
```

### Example 5: Complex Multi-Agent
```python
Query: "Weekend randonnée à Chamonix, que prendre?"

Routing: 🌤️ Weather + ✈️ Travel + 🏃 Activity

Output:
- Weather forecast for hiking days
- Complete packing list
- Hiking-specific gear
- Safety equipment
- Day-by-day recommendations
```

---

## 🛠️ Technical Implementation

### Agent Structure

```python
# Each specialist agent has:
- model: "gemini-2.5-flash"
- name: unique identifier
- description: agent expertise
- instruction: detailed system prompt
- tools: specialized FunctionTools

# Coordinator has:
- model: "gemini-2.5-flash"
- name: "coordinator"
- instruction: routing logic
- sub_agents: [all specialists]
```

### Tool Organization

Each specialist has tools relevant to its domain:
- **Weather Specialist**: `analyze_weather`, `extended_forecast`
- **Outfit Specialist**: `detailed_outfit`, `color_palette`
- **Travel Planner**: `packing_list`, `daily_outfits`
- **Activity Specialist**: `activity_gear`

---

## 🚀 Getting Started

### Test the Multi-Agent System

```bash
# Test with default query
python main.py

# Test with custom query
python main.py "Quelles couleurs porter aujourd'hui à Paris?"

# Test travel planning
python main.py "Je pars 3 jours à Nice, aide-moi à préparer ma valise"

# Test activity gear
python main.py "Équipement pour courir ce matin"
```

### Deploy to Agent Engine

```bash
# The deployment process is the same
python deploy_agent_engine.py

# The coordinator and all specialists are deployed together
```

---

## 📈 Future Enhancements

Potential new specialists to add:

- **🌍 Climate Specialist**: Long-term climate trends, seasonal advice
- **💄 Beauty Advisor**: Makeup and skincare adapted to weather
- **🏠 Home Comfort Specialist**: Indoor clothing, heating/cooling advice
- **🐕 Pet Care Specialist**: Pet clothing and outdoor safety
- **👶 Kids Specialist**: Children's clothing and safety
- **♿ Accessibility Specialist**: Adaptive clothing recommendations
- **🌱 Sustainability Specialist**: Eco-friendly clothing choices

---

## 🎓 Learning Resources

To understand the multi-agent architecture:

1. **ADK Documentation**: https://google.github.io/adk-docs/
2. **Agent Design Patterns**: See coordinator routing logic
3. **Tool Design**: Each specialist's tools in `agents/` directory
4. **System Prompts**: Read each agent's instruction for expertise design

---

## 🔧 Customization

### Adding a New Specialist

1. Create new agent file in `agents/`
2. Define specialized tools
3. Write detailed instruction prompt
4. Add to coordinator's `sub_agents`
5. Update coordinator routing logic

### Modifying Routing Logic

Edit `agents/coordinator.py`:
- Update routing keywords
- Add new specialist patterns
- Adjust routing priorities

---

## ✅ Summary

The **Multi-Agent System** provides:

✅ **5 Specialized Experts** - Each with deep domain knowledge
✅ **Intelligent Routing** - Coordinator sends queries to right specialist(s)
✅ **Better Responses** - More detailed and accurate than single agent
✅ **Scalable Architecture** - Easy to add new specialists
✅ **Complex Query Handling** - Multi-agent collaboration for complex needs
✅ **Clear Separation** - Each agent has focused responsibility

**Result**: A sophisticated, professional-grade AI system that provides expert-level advice on weather, fashion, travel, and activities!

---

**Developed for SFEIR** - Showcasing advanced multi-agent AI architecture
