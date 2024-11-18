#!/bin/bash
set -ex  # Print each command to standard output before executing it

# Start the Docker daemon in the background
    dockerd &

    # Wait for the Docker daemon to start
    until docker info >/dev/null 2>&1; do
        sleep 1
    done


# Check if run_ui.py exists in /a0
    if [ -f /a0/run_ui.py ]; then
        echo "Found run_ui.py, proceeding..."
    else
        echo "Error: run_ui.py not found in /a0"
        exit 1
    fi

# Run the dockerd-entrypoint.sh script
# /usr/local/bin/dockerd-entrypoint.sh

# Launch Agent0
python run_ui.py
