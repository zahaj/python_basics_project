import unittest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

# Import the app object from our CLI script
from daily_briefing.main import app

class TestMainCLI(unittest.TestCase):
    """Test suite for a CLI."""
    def setUp(self):
        self.runner = CliRunner()
    
    @patch("daily_briefing.main.ConfigReader")
    @patch("daily_briefing.main.OpenWeatherClient")
    @patch("daily_briefing.main.JSONPlaceholderClient")
    @patch("daily_briefing.main.DailyBriefing")
    def test_get_briefing_success(
        self, 
        mock_daily_briefing_class, 
        mock_api_client_class, 
        mock_weather_client_class, 
        mock_config_reader_class
    ):
        """Test the 'get-briefing' CLI command for a successful run."""
        # Arrange
        # --- Configure the mock DailyBriefing instance ---
        # Get a handle to the instance that will be created inside the CLI command.   
        mock_briefing_instance = mock_daily_briefing_class.return_value
        mock_briefing_instance.generate_briefing.return_value = "Good morning, Test User!"

        # Act
        # --- Invoke the CLI command ---
        # The runner calls the app, passing arguments as a list of strings.
        result = self.runner.invoke(app, ["get-briefing", "1", "--city", "Testville"])

        # Assert
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Good morning", result.stdout)
    
    @patch("daily_briefing.main.ConfigReader")
    def test_get_briefing_config_not_found(self, mock_config_reader_class):
        """Test the CLI's error handling when config.ini is missing."""

        # Arrange
        mock_config_reader_class.side_effect = FileNotFoundError("File not found")

        # Act
        result = self.runner.invoke(app, ["get-briefing", "1", "--city", "Wrocław"])

        # Assert
        # The app should handle the error gracefully and still exit with code 0.
        self.assertEqual(result.exit_code, 0)
        # Check that our user-friendly error message was printed.
        self.assertIn("Error: Configuration file 'config.ini' not found", result.stderr)
    
    @patch('daily_briefing.main.ConfigReader')
    def test_check_config_success(self, mock_config_reader_class):
        """Test the 'check-config' command for a successful run."""
        
        # Arrange
        # We just need the ConfigReader to instantiate without error.
        # The default mock behavior is fine for this.

        # Act
        result = self.runner.invoke(app, ["check-config"])
        
        # Assert
        self.assertEqual(result.exit_code, 0)
        self.assertIn("✅ Configuration file found and seems valid.", result.stdout)
        # Ensure the mock was actually used.
        mock_config_reader_class.assert_called_once()