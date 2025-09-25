"""
Command-Line Interface for the Daily Briefing application.

This module provides a CLI powered by Typer to generate briefings
and check the application's configuration.
Tu run CLI:
python -m daily_briefing.main <COMMAND>, e.g. to get a briefing:
python -m daily_briefing.main get-briefing 1 --city "Wroclaw"
To check configuration:
python -m daily_briefing.main check-config
"""
import typer
from typing_extensions import Annotated

# Import the application components
from .daily_briefing_app import DailyBriefing
from .api_interactions import JSONPlaceholderClient
from .weather_client import OpenWeatherClient
from .config_reader import ConfigReader

# Create a Typer app instance.
app = typer.Typer(
    help="A CLI application to generate a daily briefing for a user, including weather and recent posts.",
    add_completion=False,
    no_args_is_help=True  # Show help if no command is given
)

# This dependency provider function is responsible for creating the
# application instance. Our tests will mock this function directly.
def get_DailyBriefing() -> DailyBriefing:
    """Dependency to create and provide the DailyBriefing app instance."""
    config_reader = ConfigReader()
    api_client = JSONPlaceholderClient()
    weather_client = OpenWeatherClient(config_reader=config_reader)
    return DailyBriefing(api_client=api_client, weather_client=weather_client)

@app.command()
def get_briefing(
    user_id: Annotated[int, typer.Argument(
        help="The ID of the user to generate the briefing for."
    )],
    city: Annotated[str, typer.Option(
        "--city", "-c",
        help="The city for the weather forecast (e.g., 'London')."
    )]
    ):
    """
    Generates and prints a daily briefing for a specific user and city.
    """
    try:
        # --- Dependency Setup ---
        typer.echo(f"Requesting briefing for User ID: {user_id}, City: {city}...")
        briefing_app: DailyBriefing = get_DailyBriefing()
        # --- Application Execution ---
        briefing_message = briefing_app.generate_briefing(user_id=user_id, city=city)
        # --- Output ---
        typer.secho("\n--- Your Briefing ---", fg=typer.colors.CYAN, bold=True)
        typer.echo(briefing_message)

    except ValueError as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
    except (FileNotFoundError, KeyError) as e:
        typer.secho(f"Configuration Error: {e}", fg=typer.colors.RED, err=True)
    except Exception as e:
        typer.secho(f"An unexpected application error occurred: {e}", fg=typer.colors.RED, err=True)

@app.command()
def check_config():
    """
    Checks if the configuration file is present and valid.
    """
    typer.echo("Checking for 'config.ini'...")
    try:
        ConfigReader().get_api_key('openweathermap')
        success_message = "✅ Configuration file found and seems valid."
        typer.secho(success_message, fg=typer.colors.GREEN)
    except (FileNotFoundError, KeyError) as e:
        error_message = f"❌ Configuration check failed: {e}"
        typer.secho(error_message, fg=typer.colors.RED, err=True)

if __name__ == "__main__":
    app()