import configparser
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
        # Centralized Error Handling: Check for the file's existence ONCE.
        # This is called "failing fast" - we know immediately if there's a problem.
        if not self.config_file_path.is_file():
            raise FileNotFoundError(f"Configuration file not found at: {self.config_file_path.resolve()}")

        self.config = configparser.ConfigParser()
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
        try:
            api_key = self.config[service_name]['api_key'] # The dictionary-like access to the parsed data.
            return api_key
        except KeyError as err:
            # Centralized Error Handling: If the key/section is missing,
            # we provide a very clear, helpful error message.
            raise KeyError(f"Could not find api_key for service '{service_name}' in '{self.config_file_path}'. Check your config file.") from err