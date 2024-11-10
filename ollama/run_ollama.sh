#!/bin/bash
# set -x  # Enable debugging mode

echo "Starting the Ollama service on port ${OLLAMA_PORT}..."

# Start the Ollama service
if [ -x /usr/local/bin/ollama ]; then
    /usr/local/bin/ollama serve &
    echo "Ollama service started successfully."
else
    echo "/usr/local/bin/ollama not found or not executable"
    exit 1
fi

# Wait for the ollama serve command to finish initializing
sleep 30

# Check if NVIDIA GPU is available for Docker GPU support
if command -v nvidia-smi >/dev/null 2>&1; then
    echo "NVIDIA GPU detected. Starting container with GPU support."
    GPU_FLAG="--gpus=all"
else
    echo "No NVIDIA GPU detected. Please ensure NVIDIA drivers are installed on the host system."
    echo "Starting container with CPU support only."
    GPU_FLAG=""
fi

# Pull and run model inside the container
if command -v /usr/local/bin/ollama >/dev/null 2>&1; then
    
    echo "Pulling the model: ${OLLAMA_EMBED_MODEL}..."
    if ! /usr/local/bin/ollama pull "${OLLAMA_EMBED_MODEL}"; then
        echo "Pull failed. Retrying in 10 seconds..."
        sleep 10
        if ! /usr/local/bin/ollama pull "${OLLAMA_EMBED_MODEL}"; then
            echo "Pull failed again. Exiting."
            exit 1
        fi
    fi

    echo "Pulling the model: ${OLLAMA_CHAT_MODEL}..."
    if ! /usr/local/bin/ollama pull "${OLLAMA_CHAT_MODEL}"; then
        echo "Pull failed. Retrying in 10 seconds..."
        sleep 10
        if ! /usr/local/bin/ollama pull "${OLLAMA_CHAT_MODEL}"; then
            echo "Pull failed again. Exiting."
            exit 1
        fi
    fi

    echo "Running the chat model: ${OLLAMA_CHAT_MODEL}..."
    if ! /usr/local/bin/ollama run "${OLLAMA_CHAT_MODEL}"; then
        echo "Run failed. Retrying in 10 seconds..."
        sleep 10
        if ! /usr/local/bin/ollama run "${OLLAMA_CHAT_MODEL}"; then
            echo "Run failed again."
        fi
    fi &
    wait # Wait for background processes to complete
else
    echo "Error: 'ollama' command not found. Ensure Ollama was installed correctly."
fi