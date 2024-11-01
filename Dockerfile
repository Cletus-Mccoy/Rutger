# Use a base image with necessary build tools
FROM python:3.12-slim AS build

# Install necessary system packages for building Python packages
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Clone the Agent0 repository
RUN git clone https://github.com/frdel/agent-zero.git .

# Create and activate Python virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV

# Ensure the virtual environment and pip setup
RUN $VIRTUAL_ENV/bin/pip install --upgrade pip

# Install Python dependencies
RUN $VIRTUAL_ENV/bin/pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.12-slim

# Install necessary packages for SSH and Docker
RUN apt-get update && apt-get install -y \
    openssh-server \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# Create the SSH directory
RUN mkdir /var/run/sshd

# Copy the virtual environment from the build stage
COPY --from=build /opt/venv /opt/venv

# Set the PATH for the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy environment setup script
COPY set_env.sh /app/set_env.sh
RUN chmod +x /app/set_env.sh

# Expose the SSH port (default is 22)
EXPOSE 22

# Expose the WebUI port (make sure to set this variable in your docker-compose or .env)
EXPOSE ${WEB_UI_PORT}

# Start SSH service and run the setup script
CMD ["/bin/bash", "-c", "/usr/sbin/sshd && /app/set_env.sh && tail -f /dev/null"]
