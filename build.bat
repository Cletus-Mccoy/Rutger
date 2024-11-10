@echo off

REM This script is used to run the copy_env.bat script, build the docker images, and run the docker compose file

REM Run the copy_env.bat script
call copy_env.bat

REM Stop all related docker containers
docker-compose down

REM Remove all Docker images
FOR /F "tokens=*" %%i IN ('docker images -q') DO docker rmi -f %%i

REM Remove all unused containers, networks, images (both dangling and unreferenced) & volumes.
docker system prune -a --volumes -y

REM cd into the agent-zero directory and build the docker image with a specific name
docker build -t agent-zero ./agent-zero --no-cache

REM cd into the ollama directory and build the docker image with a specific name
docker build -t ollama ./ollama --no-cache

REM Run the docker-compose file with the most recent built images
docker-compose up -d

