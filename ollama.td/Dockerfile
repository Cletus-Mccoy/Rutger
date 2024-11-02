# ollama/Dockerfile
FROM python:3.12-slim

# Install necessary packages for Ollama
RUN apt-get update && apt-get install -y \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /ollama

# Expose interface
EXPOSE 11434

# Run ollama .sh script
CMD ["/bin/bash", "-c", "run_ollama.sh && tail -f /dev/null"]
