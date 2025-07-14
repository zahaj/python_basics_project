# Daily Briefing Application
A comprehensive, containerized Python application designed to provide a user with a daily summary by integrating data from multiple external sources. This project demonstrates a full backend development lifecycle, from initial design and API development to database integration, containerization, and testing.

## Key Features:
**RESTful API:** A robust API built with FastAPI to expose application logic, featuring path/query parameters and Pydantic models for data validation.
**Database Integration:** Utilizes SQLAlchemy and a PostgreSQL database to log and persist application usage data.
**Containerization:** Fully containerized using Docker and Docker Compose, allowing the API and its database to run as a reliable, multi-container service.
**Command-Line Interface:** A user-friendly CLI built with Typer allows the application to be run as a standalone tool.
**Concurrent Operations:** Implements concurrent.futures to perform multiple network requests simultaneously, significantly improving application performance.
**Comprehensive Testing:** Includes both unit and integration tests written with unittest and Pytest to ensure code quality and reliability.

## Tech Stack
**Backend:** Python, FastAPI, SQLAlchemy
**Database:** PostgreSQL
**DevOps & Tools:** Docker, Docker Compose, Git
**Testing:** Pytest, HTTPX

## Project Structure
The project follows a standard src layout to separate the installable package source from other project files like tests and configuration.
```
.
├── src/
│   └── daily_briefing/      # The main installable Python package
│       ├── __init__.py
│       ├── api_interactions.py
│       ├── config_reader.py
│       ├── daily_briefing_app.py
│       ├── database.py
│       ├── main.py          # Typer CLI logic
│       └── web_api.py       # FastAPI logic
├── tests/                   # Unit and integration tests
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile               # Docker configuration for the API
├── pyproject.toml           # Project definition and dependencies
└── README.md
```
## Setup and Installation
**Prerequisites**
Git
Docker and Docker Compose

**1. Clone the Repository**
```
git clone https://github.com/zahaj/python_basics_project.git
cd python_basics_project
```
**2. Configuration**
The application can be configured using environment variables (for Docker) or a local `config.ini` file. To run locally or provide a fallback, create a `config.ini` file in the project root.

Create a `config.ini` file from the example:
```
cp config.ini.example config.ini
```
Now, edit config.ini and add your API key from OpenWeatherMap.
```
[openweathermap]
api_key = YOUR_REAL_API_KEY_GOES_HERE
```
## Usage
**Running the Application with Docker Compose**
The primary way to run this application is with Docker Compose, which starts both the FastAPI server and the PostgreSQL database.
From the project root directory, run:
```
docker compose up --build
```
The `--build` flag ensures the Docker image is rebuilt if you've made any changes. The API will be available at `http://127.0.0.1:8000`.

**Using the REST API**

Once the application is running, you can interact with the API.

Interactive Documentation (Swagger UI):
Navigate to http://127.0.0.1:8000/docs in your browser to see the auto-generated, interactive API documentation. You can test the endpoints directly from this interface.

Example `curl` Request:
curl -X 'GET' 'http://127.0.0.1:8000/briefing/1?city=Wroclaw' -H 'accept: application/json'

Using the Command-Line Interface (CLI)
The project can also be run as a command-line tool. First, install it in editable mode in a local Python virtual environment.
```
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install the project and its dependencies
pip install -e ".[test]"
```
Now, you can use the `briefing` command:
```
briefing get-briefing 1 --city "London"
```
**Running the Tests**
The project uses Pytest for testing.

Prerequisites:
The application must be running via docker compose up for the integration tests to work.
Your local virtual environment must be activated and have the test dependencies installed (pip install -e ".[test]").

From the project root directory, run:
```
pytest
```
This will discover and run all unit and integration tests.