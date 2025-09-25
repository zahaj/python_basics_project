"""
Core application logic for generating daily briefings.

This module orchestrates the different clients (API, weather) to fetch
and assemble the data required for a user's briefing.
"""
import concurrent.futures
from typing import Optional

from .api_interactions import JSONPlaceholderClient
from .models import BriefingResponse, WeatherInfo
from .weather_client import OpenWeatherClient

class DailyBriefing:
    """
    An application class that orchestrates multiple clients to generate
    a user's daily briefing.
    """

    def __init__(self, api_client: JSONPlaceholderClient, weather_client: OpenWeatherClient):
        """
        Initializes the application with its dependencies (the clients).
        This Dependency Injection makes the class easy to test.
        """
        self.api_client = api_client
        self.weather_client = weather_client

    def generate_briefing_for_api(self, user_id: int, city: str) -> BriefingResponse:
        """
        Generates a daily briefing as a structured Pydantic object for the API.
        Fetches data concurrently and assembles it into a BriefingResponse model.

        Args:
            user_id: The ID of the user.
            city: The city for the weather forecast.

        Returns:
            A BriefingResponse object.

        Raises:
            ValueError: If the user with the given ID is not found.
        """
        # Using a ThreadPoolExecutor to run I/O-bound tasks (API calls) in parallel.
        with concurrent.futures.ThreadPoolExecutor() as executor:
            user_future = executor.submit(self.api_client.get_user, user_id)
            weather_future = executor.submit(self.weather_client.get_weather, city)
            posts_future = executor.submit(self.api_client.get_posts_by_user, user_id)

            # Wait for the most critical data first.
            user_info = user_future.result()
            if not user_info:
                raise ValueError(f"User with ID {user_id} not found.")

            # Get results from the other futures, handling potential failures gracefully.
            try:
                weather_info = weather_future.result()
            except Exception as e:
                print(f"Weather data could not be retrieved: {e}")
                weather_info = None
        
            try:        
                user_posts = posts_future.result()
            except Exception as e:
                print(f"Post data could not be retrieved: {e}")
                user_posts = None

        weather_summary = self._format_weather_summary(weather_info)
        latest_post_title = user_posts[0]['title'] if user_posts else "No new posts."

        return BriefingResponse(
            user_name=user_info.get('name', 'N/A'),
            city=city,
            weather_summary=weather_summary,
            latest_post_title=latest_post_title,            
        )
    
    def generate_briefing(self, user_id: int, city: str) -> Optional[str]:
        """
        Generates a daily briefing string suitable for CLI output.
        Fetches data concurrently and formats it into a human-readable string.

        Args:
            user_id: The ID of the user.
            city: The city for the weather forecast.

        Returns:
            A formatted string containing the briefing, or None on failure.

        Raises:
            ValueError: If the user with the given ID is not found.
        """
        try:
            response_data = self.generate_briefing_for_api(user_id, city)
            string = (
                f"Good morning, {response_data.user_name}! "
                f"{response_data.weather_summary} "
                f"Your latest post is titled: '{response_data.latest_post_title}'."
            )
            return string
        except ValueError as e:
            return str(e)
        
    def _format_weather_summary(self, weather_info: Optional[WeatherInfo]) -> Optional[str]:
        """Helper method to create a human-readable weather summary string."""
        if not weather_info:
            return "Weather data not available."
        return (
            f"The current weather in {weather_info.city} is "
            f"{weather_info.description}. It's {weather_info.temperature}°C, "
            f"but feels like {weather_info.feels_like}°C."
        )