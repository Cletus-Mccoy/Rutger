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

REM Build the docker images
docker build -t agent-zero ./agent-zero --no-cache
docker build -t ollama ./ollama



