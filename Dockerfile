# Stage 1: Use an official Python image as the base blueprint.
# Using a specific version is good practice for reproducibility.
FROM python:3.11-slim

# Set environment variables to make Python run better inside Docker.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container.
# All subsequent commands will run from this directory.
WORKDIR /app

# Copy only the project file first to leverage Docker's build cache.
COPY pyproject.toml .

# Install all dependencies defined in pyproject.toml, including fastapi and uvicorn.
# This single command installs your app and all its dependencies.
RUN pip install --no-cache-dir .

# Now, copy the rest of your application's source code.
COPY ./src/daily_briefing /app/daily_briefing

# Expose the port the container will listen on.
# Our FastAPI app will run on port 8000 inside the container.
EXPOSE 8000

# Define the command to run when a container is started from this image.
# This runs the uvicorn server. "0.0.0.0" makes it accessible from outside the container.
CMD ["uvicorn", "daily_briefing.web_api:api_app", "--host", "0.0.0.0", "--port", "8000"]