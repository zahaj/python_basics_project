# This Dockerfile defines the steps to create a container image for the FastAPI application.

# Stage 1: Use an official, lightweight Python image as the base blueprint.
# Using a specific version like 3.11-slim is good practice for reproducibility.
FROM python:3.11-slim

# Set environment variables to optimize how Python runs inside Docker.
# Prevents Python from writing .pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
# Ensures logs are sent straight to the console.
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container.
# All subsequent commands will run from this directory.
WORKDIR /app

# Copy only the project definition file first. This is a key optimization.
# Docker will cache this layer and only re-run it if pyproject.toml changes.
COPY pyproject.toml .

# Install all dependencies defined in pyproject.toml, including fastapi and uvicorn.
# This single command installs the app and all its dependencies into the container's
# Python environment.
RUN pip install --no-cache-dir .

# Now, copy the application's source code into the container.
# Because this is a separate layer, Docker won't need to reinstall all the
# dependencies for every change in the Python code.
COPY ./src/daily_briefing /app/daily_briefing

# Expose the port the container will listen on.
# The FastAPI app will run on port 8000 inside the container.
EXPOSE 8000

# Define the command to run when a container is started from this image.
# This runs the Uvicorn web server, telling it to serve the `api_app`
# object from our `web_api` module. "0.0.0.0" makes it accessible from outside the container.
CMD ["uvicorn", "daily_briefing.web_api:api_app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]