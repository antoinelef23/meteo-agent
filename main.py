"""
FastAPI server for Meteo Outfit Advisor Agent
"""
import os
import sys
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import meteo_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

# Create FastAPI app
app = FastAPI(
    title="Meteo Outfit Advisor",
    description="AI agent that recommends outfits based on weather conditions",
    version="1.0.0"
)

# Initialize ADK Runner and Session Service
session_service = InMemorySessionService()

runner = Runner(
    app_name="meteo_outfit_advisor",
    agent=meteo_agent,
    session_service=session_service
)

# Request models
class QueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = "anonymous"

class HealthResponse(BaseModel):
    status: str
    message: str
    model: str

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check"""
    return {
        "status": "healthy",
        "message": "Meteo Outfit Advisor is running!",
        "model": meteo_agent.model
    }

@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Service is operational",
        "model": meteo_agent.model
    }

@app.post("/query")
async def query_agent(request: QueryRequest):
    """
    Query the agent with a question about weather and outfit recommendations.

    Example queries:
    - "Quels vêtements pour aujourd'hui à Paris?"
    - "Je vais au travail à Lyon, qu'est-ce que je mets?"
    - "Météo pour les 5 prochains jours à Marseille"
    """
    try:
        # Create a unique session ID for this user
        user_id = request.user_id or "anonymous"
        session_id = f"session_{user_id}"

        # Create session if it doesn't exist
        existing_session = await session_service.get_session(
            app_name="meteo_outfit_advisor",
            user_id=user_id,
            session_id=session_id
        )

        if not existing_session:
            # Session doesn't exist, create it
            await session_service.create_session(
                app_name="meteo_outfit_advisor",
                user_id=user_id,
                session_id=session_id
            )

        # Create Content object with user query
        message = Content(
            role="user",
            parts=[Part(text=request.query)]
        )

        # Use Runner to invoke the agent
        events = []
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=message
        ):
            events.append(event)

        # Extract the final text response from events
        response_text = ""
        for event in events:
            if hasattr(event, 'content') and event.content:
                content = event.content
                # Check if content has parts
                if hasattr(content, 'parts'):
                    for part in content.parts:
                        # Get text from Part objects
                        if hasattr(part, 'text') and part.text:
                            response_text = part.text  # Keep the latest text response

        if not response_text:
            response_text = "No response generated"

        return {
            "query": request.query,
            "response": response_text,
            "user_id": user_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

@app.get("/info")
async def agent_info():
    """Get information about the agent"""
    return {
        "name": meteo_agent.name,
        "description": meteo_agent.description,
        "model": meteo_agent.model,
        "tools": [
            {
                "name": "get_weather_and_outfit",
                "description": "Get current weather and outfit recommendations"
            },
            {
                "name": "get_forecast_with_advice",
                "description": "Get multi-day forecast with outfit advice"
            }
        ],
        "example_queries": [
            "Quels vêtements pour aujourd'hui à Paris?",
            "Je vais au travail à Lyon, qu'est-ce que je mets?",
            "Météo pour les 5 prochains jours à Marseille",
            "Quel outfit pour faire du sport à Bordeaux?"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
