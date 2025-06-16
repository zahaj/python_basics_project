import requests
from config_reader import ConfigReader
from typing import Any, Optional, Dict
from models import WeatherInfo

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
        endpoint = f"{self.base_url}/weather"
    
        params = {
            "q": f"{city},{country_code}",
            "appid": self.api_key,
            "units": "metric" # to get Celsius temperatures
        }

        print(f"Fetching weather for '{params["q"]}' from {endpoint}")
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            weather = response.json()

            return WeatherInfo(
                city=weather['name'],
                temperature=weather['main']['temp'],
                feels_like=weather['main']['feels_like'],
                description=weather['weather'][0]['description'],
                icon_code=weather['weather'][0]['icon']
            )
            '''
            The example of successfully fetched weather dictionary:
            {
                'coord': {'lon': 17.0333, 'lat': 51.1},
                'weather': [
                    {
                        'id': 803,
                        'main': 'Clouds',
                        'description': 'broken clouds',
                        'icon': '04d'
                    }
                ],
                'base': 'stations',
                'main': {
                            'temp': 16.52,
                            'feels_like': 16.53,
                            'temp_min': 16.1,
                            'temp_max': 17,
                            'pressure': 1020,
                            'humidity': 88,
                            'sea_level': 1020,
                            'grnd_level': 1004
                },
                'visibility': 10000,
                'wind': {'speed': 9.77, 'deg': 300},
                'clouds': {'all': 75},
                'dt': 1750061420,
                'sys': {
                            'type': 2,
                            'id': 2103126,
                            'country': 'PL',
                            'sunrise': 1750041380,
                            'sunset': 1750100934
                },
                'timezone': 7200,
                'id': 3081368,
                'name': 'Wrocław',
                'cod': 200
            }
            '''
            # print(weather)
        except requests.exceptions.HTTPError as errh:
            if errh.response.status_code == 404:
                print(f"Error: City '{city}' not found.")
            else:
                print(f"Http Error: {errh}")
        except (requests.exceptions.RequestException, KeyError) as err:
            print(f"An unexpected request error occurred: {err}")
        
        return None

if __name__ == "__main__":

    config = ConfigReader()
    weather_client = OpenWeatherClient(config)
    wroclaw_weather = weather_client.get_weather("Wrocław")
    print(wroclaw_weather.city, wroclaw_weather.feels_like, wroclaw_weather.temperature)
"""
### Demonstration ###
if __name__ == "__main__":

    try:
        # This will only work if you have a valid config.ini file
        config = ConfigReader()
        weather_client = OpenWeatherClient(config)

        print("\n--- 1. Fetching weather for Wrocław ---")
        wroclaw_weather = weather_client.get_weather("Wrocław")
        if wroclaw_weather:
            main_weather = wroclaw_weather.get('weather', [{}])[0]
            main_temps = wroclaw_weather.get('main', {})
            
            city_name = wroclaw_weather.get('name')
            description = main_weather.get('description')
            temp = main_temps.get('temp')
            feels_like = main_temps.get('feels_like')

            print(f"Weather in {city_name}:")
            print(f"  - Condition: {description.capitalize()}")
            print(f"  - Temperature: {temp}°C")
            print(f"  - Feels Like: {feels_like}°C")

        print("\n--- 2. Fetching weather for a non-existent city ---")
        invalid_weather = weather_client.get_weather("NonexistentCity")
        if not invalid_weather:
            print("Correctly handled non-existent city.")

    except FileNotFoundError as e:
        print(f"\nDEMO ERROR: {e}")
        print("Please create a 'config.ini' file based on 'config.ini.example' to run the demonstration.")
    except KeyError as e:
        print(f"\nDEMO ERROR: {e}")
        print("Please ensure your 'config.ini' has the [openweathermap] section with an 'api_key'.")
"""