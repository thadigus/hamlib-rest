#!/usr/bin/env sh
# Initialize a dummy rig for debugging.

read -p "Enter web credentials username: " USERNAME
read -p "Enter web credentials password: " -s PASSWORD

echo "Initializing dummy rig for debugging..."
SESSION_ID=`curl -sS -k -u "$USERNAME":"$PASSWORD" \
  -X 'POST' \
  'http://localhost:8080/login' \
  -H 'accept: application/json' \
  -d '' | jq -r '.session_id'`
echo "Session ID: $SESSION_ID"
curl -sS -X 'POST' \
  "http://localhost:8080/rig/init?session_id=$SESSION_ID" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "model": 1,
  "port": "/dev/null",
  "baud": 9600
}' | jq -r '.status'
echo ""
echo "Dummy rig initialized."
echo "Session ID: $SESSION_ID"
