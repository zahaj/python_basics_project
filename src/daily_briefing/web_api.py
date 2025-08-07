from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from .daily_briefing_app import DailyBriefing
from .api_interactions import JSONPlaceholderClient
from .weather_client import OpenWeatherClient
from .config_reader import ConfigReader
from .models import BriefingResponse, BriefingLog as BriefingLogSchema # Use an alias to avoid name clashes
from .database import SessionLocal, create_db_and_tables, BriefingLog  as BriefingLogModel # The SQLAlchemy model

api_app = FastAPI(
    title="Daily Briefing API",
    description="An API to generate daily briefings for users.",
    version="0.1.0"
)

# --- Application Startup Event ---
# This is a FastAPI event handler that runs once when the app starts.
# It's the perfect place to create our database tables.
@api_app.on_event("startup")
def on_startup():
    create_db_and_tables()

# --- Dependency Function ---
# This generator function creates a database session for a single request,
# yields it to the endpoint, and ensures it's closed afterward.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@api_app.get("/briefing/{user_id}", response_model=BriefingResponse)
def get_user_briefing(
    user_id: int,
    city: str,
    db: Session = Depends(get_db)
):
    """
    Generates a daily briefing for a given user ID and city.
    """
    try:
        # This setup is the same as in our CLI.
        # Note: We will improve this repetitive setup later with Dependency Injection.
        config = ConfigReader()
        api_client = JSONPlaceholderClient()
        weather_client = OpenWeatherClient(config_reader=config)
        app = DailyBriefing(api_client=api_client, weather_client=weather_client)

        # --- The logic is slightly different for an API ---
        user_data = app.api_client.get_user(user_id)
        if not user_data:
            # For an API, we raise a proper HTTP error
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
        
        # The endpoint now uses the injected 'db' session directly.        
        log_entry = BriefingLogModel(user_id=user_id, city=city)
        db.add(log_entry)
        db.commit()

        weather_info = app.weather_client.get_weather(city)
        posts = app.api_client.get_posts_by_user(user_id)
        weather_summary_text = (
            f"{weather_info.temperature}°C with {weather_info.description}"
            if weather_info else "Weather data not available."
        )

       # Assemble the structured response using our Pydantic model
        return BriefingResponse(
            user_name=user_data.get('name', 'N/A'),
            city=city,
            weather_summary=weather_summary_text,
            latest_post_title=posts[0]['title'] if posts else None
        )
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Server configuration error: config.ini not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected server error occurred: {e}")
    
@api_app.get("/logs", response_model=list[BriefingLogSchema])
def get_all_logs(db: Session = Depends(get_db)):
    """Retrieve all briefing log entries from the database."""
    logs = db.query(BriefingLogModel).all()
    return logs

@api_app.get("/logs/{log_id}", response_model=BriefingLogSchema)
def get_log_by_id(log_id: int, db: Session = Depends(get_db)):
    """Retrieve a single log entry by its ID."""
    log = db.query(BriefingLogModel).filter(BriefingLogModel.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="A log with ID {log_id} not found")
    return log

# The status_code=200 specifies the HTTP status code that the API should return
# when the DELETE operation is successful.
@api_app.delete("/logs/{log_id}", status_code=200)
def delete_log_by_id(log_id: int, db: Session = Depends(get_db)):
    log_to_delete = db.query(BriefingLogModel).filter(BriefingLogModel.id == log_id).first()
    if not log_to_delete:
        raise HTTPException(status_code=404, detail="A log with ID {log_id} not found")
    
    db.delete(log_to_delete)
    db.commit()
    return {"ok": True}