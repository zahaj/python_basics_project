"""
Unit tests for the DailyBriefing application logic.
"""
import unittest
from unittest.mock import MagicMock, patch, call

from daily_briefing.daily_briefing_app import DailyBriefing
from daily_briefing.api_interactions import JSONPlaceholderClient
from daily_briefing.models import WeatherInfo, BriefingResponse
from daily_briefing.weather_client import OpenWeatherClient

class TestDailyBriefing(unittest.TestCase):
    """Test suite for testing DailyBriefing class."""

    def setUp(self):
        """
        Set up mock clients and inject them into the DailyBriefing instance.
        This runs before each test method and ensures that each test runs
        in a clean, isolated environment.
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

    @patch('daily_briefing.daily_briefing_app.concurrent.futures.ThreadPoolExecutor')
    def test_generate_briefing_for_api_success(self, mock_executor_class):
        """
        Test the successful generation of a briefing when all data is available.
        """
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

        # Configure the mock executor
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
        result = self.briefing_app.generate_briefing_for_api(user_id=3, city="Wrocław")

        # Assert
        # 1. Verify the return type is correct.
        self.assertIsInstance(result, BriefingResponse)

        # 2. Verify the attributes of the returned object.
        self.assertEqual(result.user_name, "Thomas Moore")
        self.assertEqual(result.city, "Wrocław")
        self.assertEqual(result.latest_post_title, "Latest Post Title")
        self.assertIn("cloudy", result.weather_summary)
        self.assertIn("feels like 14.0°C", result.weather_summary)

        # 3. Verify that the correct functions were submitted to the executor.
        expected_calls = [
            call(self.mock_api_client.get_user, 3),
            call(self.mock_api_client.get_posts_by_user, 3),
            call(self.mock_weather_client.get_weather, "Wrocław")
        ]
        mock_executor_instance.submit.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(mock_executor_instance.submit.call_count, 3)

    @patch('daily_briefing.daily_briefing_app.concurrent.futures.ThreadPoolExecutor')
    def test_generate_briefing_user_not_found(self, mock_executor_class):
        """
        Tests the failure case where the user ID does not exist.
        The application should raise a ValueError and not proceed.
        """
        # Arrange
        # Simulate the API client returning None for the user.
        self.mock_api_client.get_user.return_value = None

        # Configure the mock executor as before.
        mock_executor_instance = mock_executor_class.return_value.__enter__.return_value
        def mock_submit(func, *args):
            mock_future = MagicMock()
            mock_future.result.return_value = func(*args)
            return mock_future
        mock_executor_instance.submit.side_effect = mock_submit

        # Act & Assert
        # Use assertRaises as a context manager to verify that the correct
        # exception is raised and that the message is correct.
        with self.assertRaises(ValueError) as context:
            self.briefing_app.generate_briefing_for_api(user_id=999, city="Nonexistent")

        self.assertEqual(str(context.exception), "User with ID 999 not found.")

        # Verify that only the get_user method was called before the exception.
        self.mock_api_client.get_user.assert_called_once_with(999)

    @patch('daily_briefing.daily_briefing_app.concurrent.futures.ThreadPoolExecutor')
    def test_generate_briefing_graceful_failures(self, mock_executor_class):
        """
        Test graceful handling of non-critical failures (no weather or posts).
        The application should still produce a valid briefing response.
        """
        # Arrange
        self.mock_api_client.get_user.return_value = {"name": "Ervin Howell"}
        self.mock_api_client.get_posts_by_user.return_value = []  # No posts
        self.mock_weather_client.get_weather.return_value = None  # Weather service fails

        # Configure the mock executor
        mock_executor_instance = mock_executor_class.return_value.__enter__.return_value
        def mock_submit(func, *args):
            mock_future = MagicMock()
            mock_future.result.return_value = func(*args)
            return mock_future
        mock_executor_instance.submit.side_effect = mock_submit

        # Act
        result = self.briefing_app.generate_briefing_for_api(user_id=2, city="Gdańsk")

        # Assert
        # The method should still return a valid BriefingResponse object.
        self.assertIsInstance(result, BriefingResponse)

        # Check that the fallback messages are present in the response.
        self.assertEqual(result.user_name, "Ervin Howell")
        self.assertEqual(result.latest_post_title, "No new posts.")
        self.assertEqual(result.weather_summary, "Weather data not available.")