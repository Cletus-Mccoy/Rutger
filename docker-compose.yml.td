# agent-zero/docker-compose.yml
version: '3.8'

services:
  agentzero:
    build:
      context: ./agent-zero  # Build context for Agent Zero
      dockerfile: Dockerfile
    container_name: agentzero_${INSTANCE_ID}
    privileged: true
    environment:
      - API_KEY_OPENAI=${API_KEY_OPENAI}
      - INSTANCE_ID=${INSTANCE_ID}
      - WEB_UI_PORT=${WEB_UI_PORT}
    volumes:
      - ${LOCAL_AGENT_DIR}:/app
      - ./.env:/app/.env  # Mount the .env file (Eliminates the need for set_env.sh)
    ports:
      - "${WEB_UI_PORT}:80"
      - "22:22"  # Map for SSH
    networks:
      - agent_network

  ollama:
    build:
      context: ./ollama  # Build context for Ollama
      dockerfile: Dockerfile
    environment:
      - PORT=${OLLAMA_PORT} # (Do we need to map ports??)
    networks:
      - agent_network

networks:
  agent_network:
    driver: bridge
