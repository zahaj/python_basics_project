import unittest
from unittest.mock import MagicMock, patch, call

from daily_briefing.api_interactions import JSONPlaceholderClient
from daily_briefing.weather_client import OpenWeatherClient
from daily_briefing.models import WeatherInfo
from daily_briefing.daily_briefing_app import DailyBriefing

class TestDailyBriefing(unittest.TestCase):
    """Test suite for testing DailyBriefing class."""

    def setUp(self):
        """
        Set up mock clients and inject them into the DailyBriefing instance.
        This runs before each test method.
        """
        # Create mock objects for the dependencies
        # Using spec=... ensures the mock will fail if a non-existent method is called.
        self.mock_api_client = MagicMock(spec=JSONPlaceholderClient) 
        self.mock_weather_client = MagicMock(spec=OpenWeatherClient)

        # Instantiate the class under test, injecting the mocks
        self.briefing_app = DailyBriefing(
            api_client=self.mock_api_client,
            weather_client=self.mock_weather_client
        )

    # We now patch ThreadPoolExecutor where it is used.
    @patch('daily_briefing.daily_briefing_app.concurrent.futures.ThreadPoolExecutor')
    def test_generate_briefing_success_all_data(self, mock_executor_class):
        """Test the successful generation of a briefing with all data available."""
        # Arrange: Configure the return values of the mock clients' methods.
        self.mock_api_client.get_user.return_value = {"name": "Thomas Moore"}
        self.mock_api_client.get_posts_by_user.return_value = [{"title": "Latest Post Title"}]
        self.mock_weather_client.get_weather.return_value = WeatherInfo(
            city="Wrocław",
            temperature=15.5,
            feels_like=14.0, 
            description="cloudy",
            icon_code="01d"
        )

        # --- Configure the mock executor ---
        # The executor is used as a context manager, so we need to mock the __enter__ result.
        mock_executor_instance = mock_executor_class.return_value.__enter__.return_value

        # We define a side_effect to simulate the behavior of executor.submit.
        # It will call the function immediately and return a mock future holding the result.
        def mock_submit(func, *args, **kwargs):
            # In our test, just run the function immediately
            # and return a "mock future" that holds the result.
            mock_future = MagicMock()
            mock_future.result.return_value = func(*args, **kwargs)
            return mock_future

        mock_executor_instance.submit.side_effect = mock_submit

        # Act
        result = self.briefing_app.generate_briefing(user_id=3, city="Łódź")

        # Assert
        expected_briefing = (
                    f"Good morning, Thomas Moore! "
                    f"The current weather in Wrocław is cloudy. It's 15.5°C. "
                    f"Your latest post is titled: 'Latest Post Title'."
                )
        self.assertEqual(result, expected_briefing)
        self.assertIn("Good morning, Thomas Moore!", result)
        self.assertIn("weather in Wrocław is cloudy. It's 15.5°C", result)
        self.assertIn("Your latest post is titled: 'Latest Post Title'", result)

        expected_calls = [
            call(self.mock_api_client.get_user, 3),
            call(self.mock_api_client.get_posts_by_user, 3),
            call(self.mock_weather_client.get_weather, "Łódź")
        ]
        mock_executor_instance.submit.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(mock_executor_instance.submit.call_count, 3)
    
    def test_generate_briefing_user_fetch_fails(self):
        """Test that the process aborts if the initial user fetch fails."""
        # Arrange
        self.mock_api_client.get_user.return_value = None
        
        # Act
        result = self.briefing_app.generate_briefing(user_id=3, city="Łódź")

        # Assert
        self.assertEqual(result, "Could not retrieve user data. Aborting briefing.")
        # self.mock_api_client.get_posts_by_user.assert_not_called()
        # self.mock_weather_client.get_weather.assert_not_called()
    
    def test_generate_briefing_no_posts_found(self):
        """Test graceful handling of non-critical failures (no weather or posts)."""
        # Arrange
        self.mock_api_client.get_user.return_value = {"name": "Ervin Howell"}
        self.mock_api_client.get_posts_by_user.return_value = [] # No posts
        self.mock_weather_client.get_weather.return_value = None
        # Act
        result = self.briefing_app.generate_briefing(user_id=3, city="Łódź")
        # Assert
        self.assertIn("Ervin Howell", result)
        self.assertIn("no new posts.", result)
        self.assertIn("weather information", result)