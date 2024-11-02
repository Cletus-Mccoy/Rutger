#!/bin/bash

# Write the passthrough variables to the .env file
echo "API_KEY_OPENAI=${API_KEY_OPENAI}" > .env
echo "WEB_UI_PORT=${WEB_UI_PORT}" > .env


# Launch Agent0 (Needs to be added to Dockerfile after obsoletion)
python run_ui.py
