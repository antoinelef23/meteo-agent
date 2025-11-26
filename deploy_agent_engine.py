"""
Deploy Meteo Outfit Advisor Agent to Vertex AI Agent Engine

This script deploys the agent to Vertex AI Agent Engine for production use.
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    import vertexai
    from vertexai import agent_engines
    from google.cloud import storage
except ImportError as e:
    print("❌ Missing required packages. Install with:")
    print("   pip install google-cloud-aiplatform[adk,agent_engines]>=1.111")
    sys.exit(1)

# Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "lil-onboard-gcp")
LOCATION = os.getenv("AGENT_ENGINE_REGION", "europe-west1")
STAGING_BUCKET = os.getenv("STAGING_BUCKET", f"gs://{PROJECT_ID}-agent-staging")
AGENT_NAME = "meteo-outfit-advisor"

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 Checking prerequisites...")

    # Check gcloud auth
    import subprocess
    try:
        result = subprocess.run(
            ["gcloud", "auth", "list", "--filter=status:ACTIVE", "--format=value(account)"],
            capture_output=True,
            text=True,
            check=True
        )
        if not result.stdout.strip():
            print("❌ Not authenticated with gcloud. Run:")
            print("   gcloud auth application-default login")
            return False
        print(f"✅ Authenticated as: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Error checking authentication: {e}")
        return False

    # Check API keys
    from dotenv import load_dotenv
    load_dotenv()

    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  GOOGLE_API_KEY not set in .env file")
        print("   The agent needs this to work. Please add it to .env")
        return False

    if not os.getenv("WEATHERAPI_KEY"):
        print("⚠️  WEATHERAPI_KEY not set in .env file")
        print("   Get a free key at: https://www.weatherapi.com/my/")
        return False

    print(f"✅ API keys configured")
    print(f"✅ Project ID: {PROJECT_ID}")
    print(f"✅ Location: {LOCATION}")
    print(f"✅ Staging bucket: {STAGING_BUCKET}")

    return True

def create_staging_bucket():
    """Create staging bucket if it doesn't exist"""
    print(f"\n📦 Checking staging bucket: {STAGING_BUCKET}")

    try:
        storage_client = storage.Client(project=PROJECT_ID)
        bucket_name = STAGING_BUCKET.replace("gs://", "")

        try:
            bucket = storage_client.get_bucket(bucket_name)
            print(f"✅ Staging bucket exists: {bucket_name}")
        except Exception:
            print(f"Creating staging bucket: {bucket_name}")
            region = LOCATION.split("-")[0] if "-" in LOCATION else "us"
            bucket = storage_client.create_bucket(
                bucket_name,
                location=region
            )
            print(f"✅ Created staging bucket: {bucket_name}")
    except Exception as e:
        print(f"⚠️  Could not create staging bucket: {e}")
        print("   You may need to create it manually")

def deploy_agent():
    """Deploy the agent to Agent Engine"""
    print(f"\n🚀 Deploying {AGENT_NAME} to Agent Engine...")
    print("   This agent provides weather-based outfit recommendations")
    print()

    try:
        # Initialize Vertex AI
        print("Initializing Vertex AI...")
        vertexai.init(
            project=PROJECT_ID,
            location=LOCATION,
            staging_bucket=STAGING_BUCKET
        )

        # Import the agent
        print("Loading agent...")
        from agent import root_agent

        print(f"   Agent loaded: {root_agent.name}")
        print(f"   Model: {root_agent.model}")
        print(f"   Tools: {len(root_agent.tools)}")

        # Wrap agent in AdkApp
        print("Wrapping agent in AdkApp...")
        app = agent_engines.AdkApp(
            agent=root_agent,
            enable_tracing=False  # Disable tracing to reduce dependencies
        )

        # Deploy to Agent Engine
        print("Deploying to Agent Engine (this may take a few minutes)...")

        remote_app = agent_engines.create(
            agent_engine=app,
            display_name=AGENT_NAME,
            description="AI agent that recommends outfits based on weather conditions",
            requirements=["google-adk==1.14.1", "google-genai>=1.46.0", "requests>=2.31.0", "python-dotenv>=1.0.0", "python-dateutil>=2.8.0"],
            extra_packages=["agent.py", "tools"]
        )

        # Get deployment details
        resource_name = remote_app.resource_name
        resource_id = resource_name.split("/")[-1]

        print("\n" + "="*60)
        print("✅ DEPLOYMENT SUCCESSFUL!")
        print("="*60)
        print(f"Agent Name: {AGENT_NAME}")
        print(f"Resource ID: {resource_id}")
        print(f"Resource Name: {resource_name}")
        print(f"Location: {LOCATION}")
        print(f"Project: {PROJECT_ID}")
        print("\n" + "="*60)

        # Save deployment info
        import datetime
        deployment_info = f"""# Deployment Information
Agent: {AGENT_NAME}
Resource ID: {resource_id}
Resource Name: {resource_name}
Project: {PROJECT_ID}
Location: {LOCATION}
Deployed: {datetime.datetime.now().isoformat()}

# Agent Details
Name: {root_agent.name}
Model: {root_agent.model}
Tools: {len(root_agent.tools)}

# Testing the Agent
python test_agent_engine.py --resource-id {resource_id} --interactive

# Example Queries
python test_agent_engine.py --resource-id {resource_id} --query "Quels vêtements pour aujourd'hui à Paris?"
python test_agent_engine.py --resource-id {resource_id} --query "Je vais au travail à Lyon, qu'est-ce que je mets?"
python test_agent_engine.py --resource-id {resource_id} --query "Météo pour les 3 prochains jours à Marseille"

# View in Console
https://console.cloud.google.com/vertex-ai/reasoning-engines/locations/{LOCATION}?project={PROJECT_ID}

# Delete the deployment
python deploy_agent_engine.py --delete --resource-id {resource_id}
"""

        with open("deployment_info.txt", "w") as f:
            f.write(deployment_info)

        print("\n📝 Deployment info saved to: deployment_info.txt")
        print("\n🧪 Test your agent with:")
        print(f"   python test_agent_engine.py --resource-id {resource_id} --interactive")
        print("\n💡 Example queries:")
        print("   • Quels vêtements pour aujourd'hui à Paris?")
        print("   • Je vais au travail à Lyon, qu'est-ce que je mets?")
        print("   • Météo pour les 5 prochains jours à Marseille")

        return remote_app

    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def delete_agent(resource_id):
    """Delete a deployed agent"""
    print(f"\n🗑️  Deleting agent: {resource_id}")

    try:
        vertexai.init(
            project=PROJECT_ID,
            location=LOCATION,
            staging_bucket=STAGING_BUCKET
        )

        remote_app = agent_engines.get(resource_id)
        remote_app.delete(force=True)

        print(f"✅ Successfully deleted agent: {resource_id}")

    except Exception as e:
        print(f"❌ Failed to delete agent: {e}")

def main():
    """Main deployment function"""
    import argparse

    # Use module-level variables as defaults
    global PROJECT_ID, LOCATION, STAGING_BUCKET
    default_project = PROJECT_ID
    default_location = LOCATION

    parser = argparse.ArgumentParser(description="Deploy Meteo Outfit Advisor to Agent Engine")
    parser.add_argument("--delete", action="store_true", help="Delete a deployed agent")
    parser.add_argument("--resource-id", help="Resource ID for delete operation")
    parser.add_argument("--project", default=default_project, help=f"GCP Project ID (default: {default_project})")
    parser.add_argument("--location", default=default_location, help=f"Location (default: {default_location})")

    args = parser.parse_args()

    # Update global config
    PROJECT_ID = args.project
    LOCATION = args.location
    STAGING_BUCKET = f"gs://{PROJECT_ID}-agent-staging"

    print("="*60)
    print("🌤️ Meteo Outfit Advisor - Agent Engine Deployment")
    print("="*60)

    if args.delete:
        if not args.resource_id:
            print("❌ --resource-id is required for delete operation")
            sys.exit(1)
        delete_agent(args.resource_id)
        return

    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites check failed. Please fix the issues above.")
        sys.exit(1)

    # Create staging bucket
    create_staging_bucket()

    # Deploy the agent
    remote_app = deploy_agent()

    if remote_app:
        print("\n✅ All done! Your meteo agent is now running on Agent Engine.")
        print("   Users can now get weather-based outfit recommendations!")
    else:
        print("\n❌ Deployment failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
