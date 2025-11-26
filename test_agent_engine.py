"""
Test script for Meteo Outfit Advisor deployed on Agent Engine
"""

import os
import sys
import asyncio

try:
    import vertexai
    from vertexai import agent_engines
except ImportError:
    print("❌ Missing required packages. Install with:")
    print("   pip install google-cloud-aiplatform[adk,agent_engines]>=1.111")
    sys.exit(1)

# Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "lil-onboard-gcp")
LOCATION = os.getenv("AGENT_ENGINE_REGION", "europe-west1")
STAGING_BUCKET = os.getenv("STAGING_BUCKET", f"gs://{PROJECT_ID}-agent-staging")

def print_agent_info(remote_app):
    """Print information about the deployed agent"""
    print("\n" + "="*60)
    print("📊 AGENT INFORMATION")
    print("="*60)
    print(f"Resource Name: {remote_app.resource_name}")
    print(f"Display Name: {getattr(remote_app, 'display_name', 'N/A')}")
    print(f"Project: {PROJECT_ID}")
    print(f"Location: {LOCATION}")
    print("="*60 + "\n")

async def test_agent(resource_id, query=None, interactive=False):
    """Test the deployed agent"""

    try:
        # Initialize Vertex AI
        print(f"Connecting to Agent Engine...")
        vertexai.init(
            project=PROJECT_ID,
            location=LOCATION,
            staging_bucket=STAGING_BUCKET
        )

        # Get the deployed agent
        print(f"Loading agent: {resource_id}")
        remote_app = agent_engines.get(resource_id)

        print_agent_info(remote_app)

        # Create a session
        user_id = "test_user_123"
        print(f"Creating session for user: {user_id}")
        session = await remote_app.async_create_session(user_id=user_id)
        session_id = session["id"]
        print(f"✅ Session created: {session_id}\n")

        # Interactive mode
        if interactive:
            print("="*60)
            print("🤖 INTERACTIVE MODE")
            print("="*60)
            print("Ask about weather and outfit recommendations (type 'exit' to quit)")
            print("\nExample questions:")
            print("  • Quels vêtements pour aujourd'hui à Paris?")
            print("  • Je vais au travail à Lyon, qu'est-ce que je mets?")
            print("  • Météo pour les 5 prochains jours à Marseille")
            print("  • Quel outfit pour faire du sport à Nice?")
            print("="*60 + "\n")

            while True:
                try:
                    query = input("You: ").strip()
                    if query.lower() in ['exit', 'quit', 'bye']:
                        print("👋 Au revoir!")
                        break

                    if not query:
                        continue

                    await query_agent(remote_app, user_id, session_id, query)

                except KeyboardInterrupt:
                    print("\n👋 Au revoir!")
                    break

        # Single query mode
        elif query:
            await query_agent(remote_app, user_id, session_id, query)

        else:
            # Run example queries
            print("Running example queries...\n")

            example_queries = [
                "Quels vêtements pour aujourd'hui à Paris?",
                "Météo pour les 3 prochains jours à Marseille",
            ]

            for i, q in enumerate(example_queries, 1):
                print(f"\n{'='*60}")
                print(f"Example Query {i}/{len(example_queries)}")
                print(f"{'='*60}")
                await query_agent(remote_app, user_id, session_id, q)

                if i < len(example_queries):
                    print("\n⏳ Waiting 2 seconds before next query...")
                    await asyncio.sleep(2)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

async def query_agent(remote_app, user_id, session_id, query):
    """Send a query to the agent and print the response"""

    print(f"\n💬 Query: {query}")
    print(f"{'─'*60}")
    print("🌤️ Agent:")

    try:
        # Stream the response
        response_text = ""
        async for event in remote_app.async_stream_query(
            user_id=user_id,
            session_id=session_id,
            message=query
        ):
            # Print events as they arrive
            if hasattr(event, 'text') and event.text:
                print(event.text, end='', flush=True)
                response_text += event.text
            elif hasattr(event, 'content'):
                if hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            print(part.text, end='', flush=True)
                            response_text += part.text

        print()  # New line after response

        if not response_text:
            print("(No text response received)")

    except Exception as e:
        print(f"\n❌ Query failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main test function"""
    import argparse

    global PROJECT_ID, LOCATION, STAGING_BUCKET
    default_project = PROJECT_ID
    default_location = LOCATION

    parser = argparse.ArgumentParser(description="Test Meteo Outfit Advisor on Agent Engine")
    parser.add_argument("--resource-id", required=True, help="Resource ID of the deployed agent")
    parser.add_argument("--query", help="Single query to test")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--project", default=default_project, help=f"GCP Project ID (default: {default_project})")
    parser.add_argument("--location", default=default_location, help=f"Location (default: {default_location})")

    args = parser.parse_args()

    # Update global config
    PROJECT_ID = args.project
    LOCATION = args.location
    STAGING_BUCKET = f"gs://{PROJECT_ID}-agent-staging"

    print("="*60)
    print("🧪 Testing Meteo Outfit Advisor on Agent Engine")
    print("="*60)
    print(f"Project: {PROJECT_ID}")
    print(f"Location: {LOCATION}")
    print(f"Resource ID: {args.resource_id}")
    print("="*60 + "\n")

    # Run the async test
    asyncio.run(test_agent(
        resource_id=args.resource_id,
        query=args.query,
        interactive=args.interactive
    ))

if __name__ == "__main__":
    main()
