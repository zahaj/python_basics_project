import pytest
from unittest.mock import patch, MagicMock
import requests

# Import the code to be tested
from daily_briefing.weather_client import OpenWeatherClient
from daily_briefing.models import WeatherInfo

# The order of arguments is the REVERSE of the decorator stack.
@patch('daily_briefing.weather_client.requests.get')          # This is mock_requests_get
@patch('daily_briefing.weather_client.ConfigReader')        # This is mock_config_reader_class (the inner one, so it comes first)
def test_get_weather_success(mock_config_reader_class, mock_requests_get):
    """
    Tests the successful fetching and parsing of weather data using pytest.
    """
    # Arrange
    # Step 1 & 2: Get a handle to the future mock *instance* that will be
    # created when OpenWeatherClient calls ConfigReader().
    mock_config_instance = mock_config_reader_class.return_value
    # Step 3: Teach the mock instance how to behave. When its get_api_key()
    # method is called, it should return our fake key.
    mock_config_instance.get_api_key.return_value = 'fake_api_key'
    
    # (The setup for the requests mock follows the same pattern)
    mock_response = MagicMock()
    mock_response.raise_for_status().return_value = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'name': 'Wrocław',
        'main': {
            'temp': 15.0,
            'feels_like': 14.5
        },
        'weather': [{
            'description': 'clear sky',
            'icon': '01d'
        }]
    }
    mock_requests_get.return_value = mock_response

    # Act
    # Now, we create the client. Its __init__ method will use our
    # pre-configured mocks instead of real classes and functions.
    # We pass the mock instance directly, though in a more complex scenario,
    # we might let the class create it itself. For clarity, we'll let it create.
    client = OpenWeatherClient(config_reader=mock_config_instance)
    result = client.get_weather("Wrocław")
    # Assert
    # 1. Check that the result is an instance of our dataclass
    assert isinstance(result, WeatherInfo)

    # 2. Check the attributes of the returned object using dot notation
    assert result.city == "Wrocław"
    assert result.temperature == 15.0
    assert result.feels_like == 14.5
    assert result.description == "clear sky"

    # 3. Verify that the mocks were called correctly
    # Verify that the get_api_key method was called on mock instance.
    mock_config_instance.get_api_key.assert_called_once_with("openweathermap")
    # Check that requests.get was called correctly
    expected_params = {
        "q": "Wrocław,PL",
        "appid": "fake_api_key",
        "units": "metric"
    }
    mock_requests_get.assert_called_once_with(
        f"{client.base_url}/weather",
        params=expected_params,
        timeout=10
    )

@patch("daily_briefing.weather_client.requests.get")
@patch("daily_briefing.weather_client.ConfigReader")
def test_get_weather_city_not_found(mock_config_reader_class, mock_requests_get):
    """Test the graceful handling of a 404 City Not Found error."""
    # Arrange
    mock_config_instance = mock_config_reader_class.return_value
    mock_config_instance.get_api_key.return_value = "fake_api_key"
    # 1. Create the mock response that represents a 404 error.
    mock_response = MagicMock()
    mock_response.status_code = 404
    # 2. Create an actual HTTPError instance. Crucially, we pass the
    #    mock_response to it, just like the real requests library would.
    #    This ensures the error object has a .response attribute.
    http_error = requests.exceptions.HTTPError(
        "404 Client Error: Not Found", response=mock_response
    )
    # 3. Now, tell raise_for_status to raise THIS SPECIFIC, pre-configured
    #    exception object when it's called.
    mock_response.raise_for_status.side_effect = http_error
    mock_requests_get.return_value = mock_response
    
    # Act
    client = OpenWeatherClient(config_reader=mock_config_instance)
    result = client.get_weather("NonexistentCity")
    
    # Assert
    assert result is None
    mock_requests_get.assert_called_once()

