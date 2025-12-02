#!/bin/bash
# This script initializes a dummy rig for debugging purposes.
# Be sure to source this script with the following command:
# . debug/init_dummy_rig.sh
# Then you will be able to use echo $SESSION_ID to get the session ID in other scripts.

read -p "Enter web credentials username: " USERNAME
read -p "Enter web credentials password: " -s PASSWORD

echo "Initializing dummy rig for debugging..."
SESSION_ID=`curl -sS -k -u $USERNAME:$PASSWORD \
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
