#!/bin/bash

# Test the Agent Engine via REST API
PROJECT_ID="hack-ai-unified-ai-platform"
LOCATION="europe-west1"
RESOURCE_ID="7840819727810166784"
ACCESS_TOKEN=$(gcloud auth print-access-token)

echo "=========================================="
echo "🧪 Testing Agent via REST API"
echo "=========================================="
echo "Project: $PROJECT_ID"
echo "Resource ID: $RESOURCE_ID"
echo "=========================================="
echo ""

# Step 1: Create a session
echo "📝 Step 1: Creating session..."
echo "------------------------------------------"

SESSION_RESPONSE=$(curl -s -X POST \
  "https://${LOCATION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/reasoningEngines/${RESOURCE_ID}:query" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "class_method": "create_session",
    "input": {
      "user_id": "test_user_cli"
    }
  }')

echo "$SESSION_RESPONSE"

# Extract session name
SESSION_NAME=$(echo "$SESSION_RESPONSE" | grep -o '"name":"[^"]*"' | cut -d'"' -f4)

if [ -z "$SESSION_NAME" ]; then
  echo "❌ Failed to create session"
  exit 1
fi

echo ""
echo "✅ Session created: $SESSION_NAME"
echo ""

# Step 2: Query the agent
echo "💬 Step 2: Querying agent..."
echo "Query: Quels vêtements pour aujourd'hui à Paris?"
echo "------------------------------------------"

curl -X POST \
  "https://${LOCATION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/reasoningEngines/${RESOURCE_ID}:streamQuery" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"${SESSION_NAME}\",
    \"input\": \"Quels vêtements pour aujourd'hui à Paris?\"
  }"

echo ""
echo ""
echo "=========================================="
