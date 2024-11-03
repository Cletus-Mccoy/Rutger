#!/bin/bash

# Download the latest Ollama release
echo "Installing Ollama using apt..."
apt update
apt install -y ollama

# Start the Ollama container
echo "Starting the Ollama container on port $OLLAMA_PORT..."
GPU_FLAG=""
if command -v nvidia-smi >/dev/null 2>&1; then
    GPU_FLAG="--gpus=all"
    echo "NVIDIA GPU detected. Starting container with GPU support."
else
    echo "No NVIDIA GPU detected. Starting container with CPU support only."
fi

# Wait for a few seconds to let the process initialize
sleep 5

# Pull and run model inside the container 
ollama pull $OLLAMA_EMBED_MODEL
ollama run $OLLAMA_CHAT_MODEL --port "$OLLAMA_PORT" $GPU_FLAG &