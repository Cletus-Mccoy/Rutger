#!/bin/bash

set -x

echo "Starting the Ollama service on port ${OLLAMA_PORT}..."
if [ -x /usr/local/bin/ollama ]; then
    /usr/local/bin/ollama serve
    echo "/usr/local/bin/ollama not found or not executable"
    exit 1
fi

# Check if NVIDIA GPU is available for Docker GPU support
if command -v nvidia-smi >/dev/null 2>&1; then
    echo "NVIDIA GPU detected. Starting container with GPU support."
    GPU_FLAG="--gpus=all"
else
    echo "No NVIDIA GPU detected. Please ensure NVIDIA drivers are installed on the host system."
    echo "Starting container with CPU support only."
    GPU_FLAG=""
fi

# Wait for a few seconds to let the process initialize
sleep 5

# Pull and run model inside the container
if command -v /usr/local/bin/ollama >/dev/null 2>&1; then
    echo "Pulling the model: ${OLLAMA_EMBED_MODEL}..."
    /usr/local/bin/ollama pull "${OLLAMA_EMBED_MODEL}"
    
    echo "Running the chat model: ${OLLAMA_CHAT_MODEL}..."
    /usr/local/bin/ollama run "${OLLAMA_CHAT_MODEL}" --port "${OLLAMA_PORT}" ${GPU_FLAG} &  # Run in background
else
    echo "Error: 'ollama' command not found. Ensure Ollama was installed correctly."
    exit 1
fi

echo "Ollama service started successfully."

# Additional Notes:
# Ensure that the host system has the NVIDIA drivers and NVIDIA Docker support installed.
# The container must be started with the --gpus option to allow access to the GPU.
# If you need to install any specific libraries or dependencies within the container, 
# you can add those commands before starting the Ollama service.