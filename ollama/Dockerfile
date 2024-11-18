# Step 1: Use Ubuntu as the base image
FROM ubuntu:latest AS build-ollama

# Step 2: Install dependencies - bash, curl, and any other necessary tools
RUN apt-get update -y && apt-get install -y \
    bash \
    curl && \
    rm -rf /var/lib/apt/lists/*  # Clean up unnecessary package cache

# Step 3: Set the working directory 
WORKDIR /ollama

# Step 4: Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | bash
RUN chmod +x /usr/local/bin/ollama  

# Step 5: Copy the `run_ollama.sh` script into the container and set execute permissions
COPY run_ollama.sh /ollama/run_ollama.sh
RUN chmod +x /ollama/run_ollama.sh

# Step 6: Expose the Ollama service port
EXPOSE ${OLLAMA_PORT}

# Step 7: Set ENTRYPOINT to run the custom script directly
ENTRYPOINT ["/ollama/run_ollama.sh"]

# Keep the container running
CMD ["tail", "-f", "/dev/null"]