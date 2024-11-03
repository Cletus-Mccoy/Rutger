#!/bin/bash

# Download the latest Ollama release
echo "Installing Ollama using the recommended method..."

# Recommended installation method for Ollama
curl -s https://ollama.com/install.sh | bash >/dev/null 2>&1

# Check if Ollama was installed successfully
if ! command -v ollama >/dev/null 2>&1; then
    echo "Error: Unable to install Ollama. Please check the installation script or source."
    exit 1
fi

# Set default values for environment variables
OLLAMA_PORT="${OLLAMA_PORT:-11434}"  # Default port if not set
OLLAMA_EMBED_MODEL="${OLLAMA_EMBED_MODEL:-default-embed-model}"  # Default model if not set
OLLAMA_CHAT_MODEL="${OLLAMA_CHAT_MODEL:-default-chat-model}"  # Default model if not set

# Start the Ollama service
echo "Starting the Ollama service on port $OLLAMA_PORT..."
GPU_FLAG=""

# Check if NVIDIA GPU is available for Docker GPU support
if command -v nvidia-smi >/dev/null 2>&1; then
    GPU_FLAG="--gpus=all"
    echo "NVIDIA GPU detected. Starting container with GPU support."
else
    echo "No NVIDIA GPU detected. Starting container with CPU support only."
fi

# Wait for a few seconds to let the process initialize
sleep 5

# Pull and run model inside the container
if command -v ollama >/dev/null 2>&1; then
    echo "Pulling the model: $OLLAMA_EMBED_MODEL..."
    ollama pull "$OLLAMA_EMBED_MODEL"
    
    echo "Running the chat model: $OLLAMA_CHAT_MODEL..."
    ollama run "$OLLAMA_CHAT_MODEL" --port "$OLLAMA_PORT" $GPU_FLAG &
else
    echo "Error: 'ollama' command not found. Ensure Ollama was installed correctly."
    exit 1
fi

echo "Ollama service started successfully."