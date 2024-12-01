# Stage 0 (build): Build the Agent0 image
FROM python:3.12-slim AS build

# Install necessary system packages for building Python packages
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /a0

# Clone the Agent0 repository
RUN git clone https://github.com/frdel/agent-zero.git .

# Create and activate Python virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV

# Ensure the virtual environment and pip setup
RUN $VIRTUAL_ENV/bin/pip install --upgrade pip

# Install Python dependencies
RUN $VIRTUAL_ENV/bin/pip install --no-cache-dir -r requirements.txt


# Stage 1 (runtime): Set up runtime environment
FROM python:3.12-slim AS runtime

# Install Docker and other necessary tools
RUN apt-get update && apt-get install -y \
    docker.io \
    iptables \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Configure Docker for DinD
RUN mkdir /var/lib/docker
ENV DOCKER_HOST=unix:///var/run/docker.sock
ENV DOCKER_TLS_CERTDIR=/certs

# Copy the virtual environment from the build stage
COPY --from=build /opt/venv /opt/venv

# Set PATH to include virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code and other necessary files
COPY --from=build /a0 /a0

# Set the working directory
WORKDIR /a0

# Copy the modified Agent0 files
COPY /a0/run_ui.py run_ui.py
COPY /a0/initialize.py initialize.py

# Copy the modified Agent0 folders and replace their contents
COPY --chown=root:root /a0/instruments/default/ /a0/instruments/default/
COPY --chown=root:root /a0/knowledge/default/main/about/ /a0/knowledge/default/main/about/
COPY --chown=root:root /a0/prompts/ /a0/prompts/
COPY --chown=root:root /a0/python/ /a0/python/

# Copy the startup script
COPY startup.sh startup.sh
RUN chmod +x startup.sh

# Expose the WebUI port
EXPOSE ${WEB_UI_PORT}

# Add Docker entrypoint script for DinD
COPY dockerd-entrypoint.sh /usr/local/bin/dockerd-entrypoint.sh
RUN chmod +x /usr/local/bin/dockerd-entrypoint.sh

# Run the startup script
ENTRYPOINT ["/a0/startup.sh"]

# Keep the container running
CMD ["tail", "-f", "/dev/null"]