import configparser
import os # Import the 'os' module to access environment variables
from pathlib import Path # More modern way to handle file paths

class ConfigReader:
    """
    A class to read configuration settings from an INI file.
    """
    def __init__(self, config_file: str = 'config.ini'):
        """
        Initializes the ConfigReader and loads the configuration file.

        Args:
            config_file (str): The path to the configuration file.
        """
        self.config_file_path = Path(config_file)
        self.config = configparser.ConfigParser()
        if self.config_file_path.is_file():
            self.config.read(self.config_file_path)

    # Abstraction: The user of this method just asks for a key by service name.
    # They don't know it's coming from an .ini file.
    def get_api_key(self, service_name: str) -> str:
        """
        Retrieves an API key for a given service from the config file.

        Args:
            service_name (str): The section name in the INI file (e.g., 'openweathermap').

        Returns:
            The API key as a string.
            
        Raises:
            KeyError: If the service or 'api_key' is not found in the config file.
        """
        if not isinstance(service_name, str) or not service_name:
            raise TypeError("Service name must be a non-empty string")
        
        # 1. Prioritize environment variables. This is the standard 12-Factor App approach.
        # We create a standardized variable name, e.g., WEATHER_API_KEY.
        env_var_name = "WEATHER_API_KEY"
        api_key = os.getenv(env_var_name)
        if api_key:
            return api_key
        
        # 2. Fall back to the config.ini file if the environment variable is not set.
        try:
            return self.config[service_name]['api_key'] # The dictionary-like access to the parsed data.
        except KeyError as err:
            # Only raise an error if the key can't be found in ANY source.
            raise KeyError(
                f"API key for service '{service_name}' not found in environment variable "
                f"'{env_var_name}' or in the '{self.config_file_path}' file."
            )
            