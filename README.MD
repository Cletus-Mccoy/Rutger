Installer for an AI-agent based on agent-zero & ollama.

The installer will build the appropriate container by running `.\build.bat` (Windows)

**Instructions:**

1. Fill in any relevant variables in the `.env` file located in the root directory.
2. Group keys with a `# [header]` so that the `copy_env.bat` script will copy them in the correct folder when run later.
3. Run the build script to copy these variables to the appropriate containers.

The build script will call the `copy_env` script and make sure the containers have the necessary keys in the folders containing the Dockerfile.

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
