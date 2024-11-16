#!/bin/bash
set -x  # Print each command to standard output before executing it

# Check if run_ui.py exists in /a0
if [ -f /a0/run_ui.py ]; then
    echo "Found run_ui.py, proceeding..."
else
    echo "Error: run_ui.py not found in /a0"
    exit 1
fi

# Start the Docker daemon
dockerd-entrypoint.sh

# Launch Agent0
python run_ui.py
