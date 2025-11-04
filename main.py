"""
Main entry point for Meteo Outfit Advisor Agent

This module exports the root agent and provides local testing capability.
"""

import sys
import os
import asyncio

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Export for Agent Engine
__all__ = ['root_agent']

# Local testing setup
APP_NAME = "meteo_outfit_advisor"
USER_ID = "test_user"
SESSION_ID = "test_session"


async def test_agent_locally(query: str):
    """Test the agent locally with a query"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing Meteo Agent")
    print(f"{'='*60}\n")
    print(f"Query: {query}\n")
    print(f"{'─'*60}")
    print("Agent:")
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
    print("🌤️ Meteo Outfit Advisor Agent")
    print("="*60)
    print(f"Agent: {root_agent.name}")
    print(f"Model: {root_agent.model}")
    print(f"Tools: {len(root_agent.tools)}")
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

    # Example queries
    example_queries = [
        "Quels vêtements pour aujourd'hui à Paris?",
        "Je vais au travail à Lyon, qu'est-ce que je mets?",
        "Météo pour les 3 prochains jours à Marseille"
    ]

    print("Example queries:")
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
