"""
Main entry point for Meteo Outfit Advisor Agent (Multi-Agent System)

This module exports the root agent (coordinator) and provides local testing capability.
"""

import sys
import os
import asyncio

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import multi-agent system
from agents import root_agent

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Export for Agent Engine
__all__ = ['root_agent']

# Local testing setup
APP_NAME = "meteo_outfit_advisor_multiagent"
USER_ID = "test_user"
SESSION_ID = "test_session"


async def test_agent_locally(query: str):
    """Test the multi-agent system locally with a query"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing Multi-Agent Meteo System")
    print(f"{'='*60}\n")
    print(f"Query: {query}\n")
    print(f"{'─'*60}")
    print("System:")
    print(f"{'─'*60}\n")

    # Setup runner
    session_service = InMemorySessionService()
    runner = Runner(
        app_name=APP_NAME,
        agent=root_agent,
        session_service=session_service
    )

    # Create session
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    # Create message
    user_message = types.Content(parts=[types.Part(text=query)])

    # Run agent and collect response
    response_text = ""
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=user_message
    ):
        if hasattr(event, 'content') and event.content:
            if hasattr(event.content, 'parts'):
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        print(part.text, end='', flush=True)
                        response_text += part.text

    print(f"\n\n{'='*60}")
    print("✅ Test complete!")
    print(f"{'='*60}\n")

    return response_text


def main():
    """Main function for local testing"""
    print("="*60)
    print("🌤️ Meteo Outfit Advisor - Multi-Agent System")
    print("="*60)
    print(f"Coordinator: {root_agent.name}")
    print(f"Model: {root_agent.model}")
    print(f"Specialist Agents: {len(root_agent.sub_agents)}")
    print()
    print("🤖 Specialist Team:")
    for i, agent in enumerate(root_agent.sub_agents, 1):
        print(f"   {i}. {agent.name} - {agent.description}")
    print()

    # Check environment variables
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY")
    weather_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        print("⚠️  GOOGLE_API_KEY not set in .env file")
        print("   Please copy .env.example to .env and add your API key")
        return

    if not weather_key:
        print("⚠️  OPENWEATHER_API_KEY not set in .env file")
        print("   Get a free key at: https://openweathermap.org/api")
        print("   Then add it to your .env file")
        return

    print("✅ Environment configured")
    print()

    # Example queries showing different agents
    example_queries = [
        "🌤️  Quelle est la météo détaillée à Paris?",
        "👔 Quelles couleurs porter aujourd'hui à Lyon?",
        "✈️  Je pars 3 jours à Marseille, aide-moi à préparer ma valise",
        "🏃 Équipement pour courir ce matin à Nice?"
    ]

    print("Example queries (different specialists):")
    for i, query in enumerate(example_queries, 1):
        print(f"  {i}. {query}")
    print()

    # Interactive or example mode
    import sys
    if len(sys.argv) > 1:
        # Use command line argument as query
        query = " ".join(sys.argv[1:])
        asyncio.run(test_agent_locally(query))
    else:
        # Run first example
        print("Running example query (use 'python main.py \"your query\"' for custom queries)\n")
        asyncio.run(test_agent_locally(example_queries[0]))


if __name__ == "__main__":
    main()
