# ollama/entrypoint.sh
#!/bin/bash

# Pull the latest Ollama Docker image
echo "Pulling the latest Ollama Docker image..."
docker pull ollama/ollama

# Start the Ollama container
echo "Starting the Ollama container on port $OLLAMA_PORT..."
GPU_FLAG=""
if command -v nvidia-smi >/dev/null 2>&1; then
    GPU_FLAG="--gpus=all"
    echo "NVIDIA GPU detected. Starting container with GPU support."
else
    echo "No NVIDIA GPU detected. Starting container with CPU support only."
fi

# Run the Ollama container with specified configuration
docker run -d $GPU_FLAG -p "$OLLAMA_PORT:11434" --name ollama ollama/ollama

# Wait for a few seconds to let the container initialize
sleep 5

# Pull and run model inside the container (TODO)
# pull nomic
# run llama3.2:8b