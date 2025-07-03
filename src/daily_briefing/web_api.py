from fastapi import FastAPI

from fastapi import HTTPException
from .daily_briefing_app import DailyBriefing
from .api_interactions import JSONPlaceholderClient
from .weather_client import OpenWeatherClient
from .config_reader import ConfigReader
from .models import BriefingResponse

api_app = FastAPI(
    title="Daily Briefing API",
    description="An API to generate daily briefings for users.",
    version="0.1.0"
)

@api_app.get("/briefing/{user_id}", response_model=BriefingResponse)
def get_user_briefing(user_id: int, city: str):
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