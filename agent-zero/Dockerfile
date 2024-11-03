# Description: Dockerfile for building the Agent0 container image     

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

# Stage 1 (runtime): Create a minimal image with the virtual environment and necessary packages
FROM python:3.12-slim AS runtime

    # Install necessary packages for SSH and Docker
    RUN apt-get update && apt-get install -y \
        openssh-server \
        docker.io \
        && rm -rf /var/lib/apt/lists/*

    # Create the SSH directory
    RUN mkdir /var/run/sshd

    # Copy the virtual environment from the build stage
    COPY --from=build /opt/venv /opt/venv

    # Copy all files from the build stage to /a0 in the final stage
    COPY --from=build /a0 /a0

    # Set the PATH for the virtual environment
    ENV PATH="/opt/venv/bin:$PATH"

    # Set the working directory
    WORKDIR /a0

    # Copy environment setup script
    COPY set_env.sh /a0/set_env.sh
    RUN chmod +x /a0/set_env.sh

    # Expose the SSH port
    EXPOSE 22

    # Expose the WebUI port (make sure to copy example.env to .env)
    EXPOSE ${WEB_UI_PORT}

    # Set the entrypoint to ensure the script runs correctly
    ENTRYPOINT ["/a0/set_env.sh"]

    # Start the SSH service in the background and keep the container running
    CMD ["service", "ssh", "start"]
