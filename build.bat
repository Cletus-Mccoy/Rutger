@echo off

REM This script is used to run the copy_env.bat script, build the docker images, and run the docker compose file

REM Run the copy_env.bat script
call copy_env.bat
REM cd into the agent-zero directory and build the docker image with a specific name
cd agent-zero
docker build --no-cache -t agent-zero-image .

REM cd into the ollama directory and build the docker image with a specific name
cd ..
cd ollama
docker build --no-cache -t ollama-image .

REM cd into the root directory and run the docker compose file
cd ..
docker-compose up -d