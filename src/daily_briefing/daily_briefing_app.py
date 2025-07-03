
from typing import Optional
import concurrent.futures

from .api_interactions import JSONPlaceholderClient
from .weather_client import OpenWeatherClient, ConfigReader
# from config_reader import ConfigReader
from .models import WeatherInfo

class DailyBriefing:
    """
    An application class that orchestrates multiple clients to generate
    a user's daily briefing.
    """

    def __init__(self, api_client: JSONPlaceholderClient, weather_client: OpenWeatherClient):
        """
        Initializes the application with its dependencies (the clients).
        This is called Dependency Injection and makes the class easy to test.
        """
        self.api_client = api_client
        self.weather_client = weather_client
    
    def generate_briefing(self, user_id: int, city: str) -> Optional[str]:
        """
        Generates a daily briefing string by fetching data concurrently.
        """      


        print(f"\n--- Generating daily briefing for user {user_id} in {city} ---")
        

        with concurrent.futures.ThreadPoolExecutor() as executor:
            user_future = executor.submit(self.api_client.get_user, user_id)
            weather_future = executor.submit(self.weather_client.get_weather, city)
            posts_future = executor.submit(self.api_client.get_posts_by_user, user_id)

        try:
            user_info = user_future.result()
        except Exception as e:
            print(f"Error fetching user data: {e}")
            user_info = None
        
        if not user_info:
            return "Could not retrieve user data. Aborting briefing."

        user_name = user_info.get("name", "there")

        try:
            weather_info = weather_future.result()
        except Exception as e:
            print(f"Error fetching weather: {e}")
            weather_info = None
        
        try:        
            user_posts = posts_future.result()
            latest_post_title = user_posts[0].get("title") if user_posts else None
        except Exception as e:
            print(f"Error fetching posts: {e}")
            latest_post_title = None

        briefing = f"Good morning, {user_name}! "
        if weather_info:
            briefing += f"The current weather in {weather_info.city} is {weather_info.description}. It's {weather_info.temperature}°C. "
        else:
            briefing += f"Could not retrieve weather information. "
        if latest_post_title:        
            briefing += f"Your latest post is titled: '{latest_post_title}'."
        else:
            briefing += f"You have no new posts."

        return briefing

# --- Demonstration Section ---
if __name__ == "__main__":
    try:
        # Setup dependencies
        config_reader = ConfigReader()
        api_client = JSONPlaceholderClient()
        weather_client = OpenWeatherClient(config_reader=config_reader)
        
        # Inject dependencies into the application
        app = DailyBriefing(api_client=api_client, weather_client=weather_client)
        
        # Run the workflow
        user_briefing = app.generate_briefing(user_id=1, city="Wroclaw")
        if user_briefing:
            print("\n--- Your Briefing ---")
            print(user_briefing)
    except (FileNotFoundError, KeyError) as e:
        print(f"\nDEMO ERROR: {e}")
        print("Please ensure your 'config.ini' is set up correctly.")