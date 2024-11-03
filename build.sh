#!/bin/bash


# This script is used to build the docker images and run the docker compose file

#  cd into the agent-zero directory and build the docker image
cd agent-zero
docker build --no-cache.

# cd into the ollama directory and build the docker image
cd ..
cd ollama
docker build --no-cache.


# cd into the root directory and run the docker compose file
cd ..
docker compose up -d 