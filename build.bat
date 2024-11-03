@echo off

REM This script is used to run the copy_env.bat script, build the docker images, and run the docker compose file

REM Run the copy_env.bat script
call copy_env.bat

REM Remove all unused containers, networks, images (both dangling and unreferenced) & volumes.
docker system prune -f

REM cd into the agent-zero directory and build the docker image with a specific name
docker build --no-cache -t agent-zero ./agent-zero

REM cd into the ollama directory and build the docker image with a specific name
docker build --no-cache -t ollama ./ollama

REM Run the docker-compose file
docker-compose up -d

