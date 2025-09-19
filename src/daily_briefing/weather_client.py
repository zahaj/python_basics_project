"""
Client for interacting with the OpenWeatherMap API.

This module handles making requests to the OpenWeatherMap service to fetch
current weather data for a specified location.
"""
import logging
from typing import Optional

import requests

from .config_reader import ConfigReader
from .models import WeatherInfo

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OpenWeatherClient:
    """ A client to interact with the OpenWeatherMap API."""

    def __init__(self, config_reader: ConfigReader, base_url: str = "https://api.openweathermap.org/data/2.5/"):
        """
        Initializes the client.

        Args:
            config_reader (ConfigReader): An instance of ConfigReader to get API keys.
            base_url (str): The base URL for the API.
        """        
        self.base_url = base_url
        self.api_key = config_reader.get_api_key("openweathermap")

    def get_weather(self, city: str, country_code: str = 'PL') -> Optional[WeatherInfo]:
        """
        Fetches the current weather for a given city.
        
        Args:
            city (str): The name of the city.
            country_code (str): The ISO 31166 country code.
        
        Returns:
            A WeatherInfo object if successful, otherwise None.
        """
        params = {
            "q": f"{city},{country_code}",
            "appid": self.api_key,
            "units": "metric" # to get Celsius temperatures
        }
        logging.info(f"Fetching weather for {params['q']} from {self.base_url}/weather...")
        try:
            response = requests.get(f"{self.base_url}/weather", params=params, timeout=10)
            response.raise_for_status()
            weather = response.json()
            # Example API response:
            # {
            #     "coord": {"lon": 17.0333, "lat": 51.1},
            #     "weather": [
            #         {
            #             "id": 803,
            #             "main": "Clouds",
            #             "description": "broken clouds",
            #             "icon": "04d"
            #         }
            #     ],
            #     "base": "stations",
            #     "main": {
            #         "temp": 16.52,
            #         "feels_like": 16.53,
            #         "temp_min": 16.1,
            #         "temp_max": 17,
            #         "pressure": 1020,
            #         "humidity": 88,
            #         "sea_level": 1020,
            #         "grnd_level": 1004
            #     },
            #     "visibility": 10000,
            #     "wind": {"speed": 9.77, "deg": 300},
            #     "clouds": {"all": 75},
            #     "dt": 1750061420,
            #     "sys": {
            #         "type": 2,
            #         "id": 2103126,
            #         "country": "PL",
            #         "sunrise": 1750041380,
            #         "sunset": 1750100934
            #     },
            #     "timezone": 7200,
            #     "id": 3081368,
            #     "name": "Wrocław",
            #     "cod": 200
            # }

            # Create and return a structured WeatherInfo object
            return WeatherInfo(
                city=weather['name'],
                temperature=weather['main']['temp'],
                feels_like=weather['main']['feels_like'],
                description=weather['weather'][0]['description'],
                icon_code=weather['weather'][0]['icon']
            )
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logging.warning(f"City '{city}' not found.")
            else:
                logging.error(f"HTTP error fetching weather for {city}: {e}")
        except (requests.exceptions.RequestException, KeyError) as e:
            # KeyError could happen if the response JSON is malformed
            logging.error(f"An unexpected error occurred fetching weather for {city}: {e}")
        return None