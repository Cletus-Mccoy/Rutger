# Use a lightweight Python base image
FROM python:3.12-slim

# Install necessary packages for Ollama
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -sSfL https://ollama.com/download.sh | sh

# Set the working directory for the Ollama application
WORKDIR /ollama

# Copy the Ollama setup script into the container
COPY run_ollama.sh /ollama/run_ollama.sh
RUN chmod +x /ollama/run_ollama.sh

# Expose the Ollama service port
EXPOSE 11434

# Use an entrypoint script to handle both setup and interactive sessions
ENTRYPOINT ["/bin/bash", "-c", "/ollama/run_ollama.sh; exec /bin/bash"]
