import requests
from config_reader import ConfigReader
from typing import Any, Optional, Dict 

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

    def get_weather(self, city: str, country_code: str = 'PL') -> Optional[Dict[str, Any]]:
        """
        Fetches the current weather for a given city.
        
        Args:
            city (str): The name of the city.
            country_code (str): The ISO 31166 country code.
        
        Returns:
            A dictionary with weather data if successful, otherwise None.
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
            print(weather)
            return weather
        except requests.exceptions.HTTPError as errh:
            if errh.response.status_code == 404:
                print(f"Error: City '{city}' not found.")
            else:
                print(f"Http Error: {errh}")
        except requests.exceptions.RequestException as err:
            print(f"An unexpected request error occurred: {err}")
        return None


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