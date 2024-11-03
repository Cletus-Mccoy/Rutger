#!/bin/bash
set -x  # Print each command to standard output before executing it

echo "Current directory: $(pwd)"
echo "Listing contents of /a0:"
ls -l /a0

# Write the passthrough variables to the .env file
echo "API_KEY_OPENAI=${API_KEY_OPENAI}" > .env
echo "WEB_UI_PORT=${WEB_UI_PORT}" > .env

# Print the environment variables
echo "Environment variables:"
env

# Check if run_ui.py exists in /a0
if [ -f /a0/run_ui.py ]; then
    echo "Found run_ui.py, proceeding..."
else
    echo "Error: run_ui.py not found in /a0"
    exit 1
fi

# Launch Agent0 (Needs to be added to Dockerfile after obsoletion)
python run_ui.py
