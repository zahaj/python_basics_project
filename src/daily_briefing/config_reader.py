"""
Handles reading configuration settings for the application.

This module provides a centralized way to access configuration, prioritizing
environment variables over a local `config.ini` file.
"""
import configparser
import os
from pathlib import Path

class ConfigReader:
    """
    Reads configuration from environment variables or a fallback .ini file.
    """
    def __init__(self, config_file: str = 'config.ini'):
        """
        Initializes the ConfigReader.

        Args:
            config_file (str): The path to the fallback configuration file.
        """
        self.config_file_path = Path(config_file)
        self.config = configparser.ConfigParser()
        
        if self.config_file_path.is_file():
            self.config.read(self.config_file_path)
        # Note: No error is raised if the file doesn't exist, allowing the
        # application to run in environments that only use environment variables.

    def get_api_key(self, service_name: str) -> str:
        """
        Retrieves an API key, prioritizing environment variables.

        This method first checks for a standardized environment variable. If not
        found, it falls back to the `config.ini` file. This is useful for
        local development with the CLI.

        Args:
            service_name: The section name in the INI file (e.g., 'openweathermap').

        Returns:
            The API key as a string.

        Raises:
            KeyError: If the API key is not found in any source.
            TypeError: If the service_name is not a valid string.
        """
        if not isinstance(service_name, str) or not service_name:
            raise TypeError("Service name must be a non-empty string")
        
        # 1. Prioritize environment variables.
        # Standardized environment variable name for the weather API key.
        env_var_name = "WEATHER_API_KEY"
        api_key = os.getenv(env_var_name)
        if api_key:
            return api_key
        
        # 2. Fall back to the config.ini file if the environment variable is not set.
        try:
            return self.config[service_name]['api_key']
        except KeyError as err:
            # Only raise an error if the key can't be found in ANY source.
            raise KeyError(
                f"API key for service '{service_name}' not found in environment variable "
                f"'{env_var_name}' nor in the '{self.config_file_path}' file."
            )