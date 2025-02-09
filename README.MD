# AI Agent Environment Setup

This project sets up an AI agent environment using agent-zero and ollama in Docker containers.

## Setup Instructions

1. Clone this repository
2. Configure environment variables:
   - Edit the `.env` file in the root directory
   - Variables are grouped using `# [header]` format
   - Required sections:
     - `[Local]` - Instance configuration
     - `[ollama]` - Ollama model settings
     - `[agent-zero]` - Agent configuration

3. Build the environment:
   - Windows: Run `.\build.bat`
   - This will:
     - Copy environment variables to required locations
     - Build Docker images
     - Start containers using docker-compose

## Environment Structure

The environment consists of two main components:
- Ollama: Runs the AI models
- Agent-Zero: Handles agent orchestration

## Container Setup

The build script will call the `copy_env` script which in turn will make sure the containers have the necessary keys in a .env file in the folders containing the Dockerfile.

The script will continue with building the specified images using the Dockerfiles:
```bash
REM cd into the agent-zero directory and build the docker image with a specific name
docker build --no-cache -t agent-zero ./agent-zero
```

Finally, the script will run the containers using a compose file in daemon mode:
```bash
REM Run the docker-compose file
docker-compose up -d
```

Todo:

* reinforcement learning
* production server 
* hosting
