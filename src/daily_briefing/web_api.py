"""
Defines the main FastAPI application, its endpoints, and dependencies.

This module is the entry point for the web server and orchestrates the
entire API functionality, including routing, dependency injection, and
request/response handling.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import auth
from .api_interactions import JSONPlaceholderClient
from .config_reader import ConfigReader
from .daily_briefing_app import DailyBriefing
from .database import SessionLocal, create_db_and_tables, BriefingLog as BriefingLogModel
from .models import BriefingResponse, BriefingLog as BriefingLogSchema
from .weather_client import OpenWeatherClient

# --- Lifespan Event Handler ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    This is the recommended way to manage resources like database tables.
    """
    print("Application startup: Creating database tables...")
    create_db_and_tables()
    yield
    print("Application shutdown.")

# Initialize the main FastAPI application object
api_app = FastAPI(
    title="Daily Briefing API",
    description="An API to generate daily briefings for users, including weather and posts.",
    version="1.0.0",
    lifespan=lifespan
)


# --- FAKE USER DATABASE (for demonstration) ---
# In a real app, this would be a user table in the database.
# The password hash was generated using: auth.get_password_hash("testpassword")
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "hashed_password": "$2b$12$oK1WqVEz3K0xgXVFj9s9cOsoZU1wy9/nk/24LeQVhpQImJuFn2LiG"
    }
}


# --- DEPENDENCY FUNCTIONS ---

def get_db():
    """
    FastAPI dependency that provides a database session for a single request.
    Ensures the session is always closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_config_reader() -> ConfigReader:
    return ConfigReader()

def get_api_client() -> JSONPlaceholderClient:
    return JSONPlaceholderClient()

def get_weather_client(config: ConfigReader = Depends(get_config_reader)) -> OpenWeatherClient:
    return OpenWeatherClient(config_reader=config)

def get_briefing_app(
    api_client: JSONPlaceholderClient = Depends(get_api_client),
    weather_client: OpenWeatherClient = Depends(get_weather_client)
) -> DailyBriefing:
    return DailyBriefing(api_client=api_client, weather_client=weather_client)


# --- API ENDPOINTS ---

@api_app.post("/token", tags=["Authentication"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates a user and returns a JWT access token.
    This is the standard OAuth2 password flow endpoint.
    """    
    user = fake_users_db.get(form_data.username)
    if not user or not auth.verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@api_app.get("/briefing/{user_id}", response_model=BriefingResponse, tags=["Briefing"])
def get_user_briefing(
    user_id: int,
    city: str,
    db: Session = Depends(get_db),
    app: DailyBriefing = Depends(get_briefing_app)
):
    """
    Generates and returns a daily briefing for a given user ID and city.

    This endpoint orchestrates calls to external services to gather user data,
    weather information, and recent posts, then combines them into a
    structured response. It also logs the request to the database.
    """
    try:
        briefing = app.generate_briefing_for_api(user_id=user_id, city=city)

        # Log the successful briefing request to the database.       
        log_entry = BriefingLogModel(user_id=user_id, city=city)
        db.add(log_entry)
        db.commit()

        return briefing

    except ValueError as e:
        # This catches specific application errors, like a user not being found.
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # It's good practice to have a catch-all for unexpected errors.
        raise HTTPException(status_code=500, detail="An unexpected server error occurred: {e}.")

@api_app.get("/logs", response_model=list[BriefingLogSchema], tags=["Logs"])
def get_all_logs(
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
    ):
    """
    (Protected) Retrieves all briefing log entries from the database.
    Requires a valid JWT access token.
    """
    logs = db.query(BriefingLogModel).all()
    return logs

@api_app.get("/logs/{log_id}", response_model=BriefingLogSchema, tags=["Logs"])
def get_log_by_id(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
    ):
    """
    (Protected) Retrieves a single log entry by its ID.
    Requires a valid JWT access token.
    """
    log = db.query(BriefingLogModel).filter(BriefingLogModel.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="A log with ID {log_id} not found")
    return log

@api_app.delete("/logs/{log_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Logs"])
def delete_log_by_id(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
    ):
    """
    (Protected) Deletes a log entry by its ID.
    Returns a 204 No Content status on successful deletion.
    Requires a valid JWT access token.
    """
    log_to_delete = db.query(BriefingLogModel).filter(BriefingLogModel.id == log_id).first()
    if not log_to_delete:
        raise HTTPException(status_code=404, detail="A log with ID {log_id} not found")
    
    db.delete(log_to_delete)
    db.commit()
    
    # A 204 response should have no body, so we return None.
    return None