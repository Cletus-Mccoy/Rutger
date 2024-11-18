@echo off

REM This script is used to run the copy_env.bat script, build the docker images, and run the docker compose file

REM Run the copy_env.bat script
call copy_env.bat

REM Stop all related docker containers
docker-compose down

REM Remove Docker images related to the docker-compose file in this folder
FOR /F "tokens=*" %%i IN ('docker-compose images -q') DO docker rmi -f %%i

REM Remove all unused containers, networks, images (both dangling and unreferenced) & volumes.
docker system prune -a --volumes

REM cd into the agent-zero directory and build the docker image with a specific name
REM docker build -t agent-zero ./agent-zero
docker build -t agent-zero ./DinD --no-cache

REM cd into the ollama directory and build the docker image with a specific name
docker build -t ollama ./ollama

REM Run the docker-compose file with the most recent built images
docker-compose up -d

