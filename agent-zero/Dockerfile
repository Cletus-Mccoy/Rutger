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

    RUN apt-get update && apt-get install -y \
        docker.io \
        && rm -rf /var/lib/apt/lists/*

    # Copy the virtual environment from the build stage
    COPY --from=build /opt/venv /opt/venv

    # Set PATH to include virtual environment
    ENV PATH="/opt/venv/bin:$PATH"

    # Copy application code and other necessary files
    COPY --from=build /a0 /a0

    # Set the working directory 
    WORKDIR /a0

    # Copy the modified Agent0 files
    COPY run_ui.py run_ui.py
    COPY initialize.py initialize.py
    COPY /prompts/default /prompts/default
    
    # Copy the startup script and set execute permissions
    COPY startup.sh /a0/startup.sh
    RUN chmod +x /a0/startup.sh

    # Expose the WebUI port
    EXPOSE ${WEB_UI_PORT}

    # Entrypoint: Execute startup.sh
    ENTRYPOINT ["/a0/startup.sh"]
    
    # Keep the container running
    CMD ["tail", "-f", "/dev/null"]

    
