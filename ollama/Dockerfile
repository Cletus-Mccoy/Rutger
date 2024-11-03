# ollama/Dockerfile
FROM python:3.12-slim

# Install necessary packages for Ollama
RUN apt-get update && apt-get install -y \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /ollama

# Copy ollama setup script 
COPY run_ollama.sh /ollama/run_ollama.sh
RUN chmod +x /ollama/run_ollama.sh

# Expose interface
EXPOSE 11434

# Run ollama .sh script
CMD ["/bin/bash", "-c", "/ollama/run_ollama.sh && tail -f /dev/null"]
