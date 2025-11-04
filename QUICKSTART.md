# Quick Start - Meteo Outfit Advisor

Déployez votre agent de recommandation vestimentaire en 5 minutes! 🚀

---

## 🎯 Setup Initial (2 minutes)

### 1. Obtenir les clés API

#### Gemini API (gratuit)
1. Aller sur: https://aistudio.google.com/apikey
2. Créer une clé API
3. Copier la clé

#### OpenWeatherMap API (gratuit)
1. Aller sur: https://openweathermap.org/api
2. S'inscrire (gratuit)
3. Créer une clé API
4. Copier la clé

### 2. Configuration

```bash
cd weather_app  # or wherever you cloned the repo

# Copier le template
cp .env.example .env

# Éditer .env et ajouter vos clés
nano .env  # ou vim, code, etc.

# Contenu de .env:
# GOOGLE_API_KEY=votre_clé_gemini_ici
# OPENWEATHER_API_KEY=votre_clé_openweather_ici
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 🧪 Test Local (30 secondes)

```bash
# Test rapide
python main.py

# Test avec votre question
python main.py "Quels vêtements pour aujourd'hui à Paris?"
```

**Ça marche? Parfait! Passons au déploiement sur Agent Engine.** ✅

---

## 🚀 Déploiement sur Agent Engine (2 minutes)

### 1. Authentification GCP

```bash
gcloud auth login
gcloud auth application-default login

export GOOGLE_CLOUD_PROJECT="lil-onboard-gcp"
gcloud config set project $GOOGLE_CLOUD_PROJECT
```

### 2. Activer les APIs

```bash
gcloud services enable \
    aiplatform.googleapis.com \
    storage.googleapis.com
```

### 3. Déployer!

```bash
python deploy_agent_engine.py
```

**Attendez 2-3 minutes... ⏳**

**Résultat:**
```
============================================================
✅ DEPLOYMENT SUCCESSFUL!
============================================================
Agent Name: meteo-outfit-advisor
Resource ID: 1234567890123456789
...
```

### 4. Tester l'agent déployé

```bash
# Copier le Resource ID du déploiement ci-dessus
python test_agent_engine.py --resource-id VOTRE_RESOURCE_ID --interactive
```

---

## 💬 Essayez ces Questions

En mode interactif, essayez:

```
• Quels vêtements pour aujourd'hui à Paris?
• Je vais au travail à Lyon, qu'est-ce que je mets?
• Quel outfit pour faire du sport à Nice?
• Météo pour les 5 prochains jours à Marseille
• Comment m'habiller pour un événement formel à Bordeaux?
```

---

## 🎉 C'est Tout!

Votre agent est maintenant:
- ✅ Déployé sur Agent Engine
- ✅ Accessible via API
- ✅ Auto-scalable
- ✅ Monitoré automatiquement

---

## 📊 Gestion de l'Agent

### Voir les déploiements

```bash
# Via la console
open "https://console.cloud.google.com/vertex-ai/reasoning-engines?project=lil-onboard-gcp"
```

### Supprimer un déploiement

```bash
python deploy_agent_engine.py --delete --resource-id RESOURCE_ID
```

---

## 🐛 Problèmes?

### "API key not configured"
```bash
# Vérifier .env
cat .env

# Doit contenir:
# GOOGLE_API_KEY=...
# OPENWEATHER_API_KEY=...
```

### "Permission denied"
```bash
gcloud auth application-default login
```

### "City not found"
- Essayer avec le code pays: "Paris,FR"
- Vérifier l'orthographe

---

## 📚 Documentation Complète

Pour plus de détails, voir:
- `README.md` - Documentation complète
- `AGENT_ENGINE_DEPLOYMENT_GUIDE.md` - Guide de déploiement avancé

---

## 🆘 Commandes de Référence Rapide

```bash
# Test local
python main.py "votre question"

# Déployer
python deploy_agent_engine.py

# Tester agent déployé
python test_agent_engine.py --resource-id ID --interactive

# Supprimer
python deploy_agent_engine.py --delete --resource-id ID
```

---

**Bon courage! 🌤️👔**
