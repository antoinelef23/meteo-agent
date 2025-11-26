"""
Simple test script for Agent Engine without sessions
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

import vertexai
from vertexai import agent_engines

# Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "hack-ai-unified-ai-platform")
LOCATION = "europe-west1"
RESOURCE_ID = "2542334766208778240"

def test_agent_simple():
    """Test agent with direct query"""
    print("="*60)
    print("🧪 Simple Agent Test")
    print("="*60)
    print(f"Project: {PROJECT_ID}")
    print(f"Location: {LOCATION}")
    print(f"Resource ID: {RESOURCE_ID}")
    print("="*60)

    # Initialize Vertex AI
    print("\nInitializing Vertex AI...")
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    # Get the agent
    print(f"Loading agent: {RESOURCE_ID}")
    resource_name = f"projects/{PROJECT_ID}/locations/{LOCATION}/reasoningEngines/{RESOURCE_ID}"

    try:
        remote_app = agent_engines.get(resource_name)
        print(f"✅ Agent loaded successfully")
        print(f"   Display Name: {remote_app.display_name}")
        print(f"   Resource Name: {remote_app.resource_name}")

        # Try a simple query using stream_query
        print("\n" + "="*60)
        print("📊 Testing agent query...")
        print("="*60)

        query = "Quels vêtements pour aujourd'hui à Paris?"
        print(f"\n💬 Query: {query}")
        print("-" * 60)

        # Create a session first
        print("\nCreating session...")
        session = remote_app.create_session(user_id="test_user")
        print(f"✅ Session created: {session.name}")

        # Use stream_query
        print("\n🌤️ Response:")
        print("-" * 60)

        for chunk in remote_app.stream_query(
            session_id=session.name,
            input=query
        ):
            if hasattr(chunk, 'text') and chunk.text:
                print(chunk.text, end='', flush=True)
            elif hasattr(chunk, 'content'):
                print(chunk.content, end='', flush=True)

        print("\n" + "-" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    success = test_agent_simple()
    sys.exit(0 if success else 1)
