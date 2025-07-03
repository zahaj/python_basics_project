import typer
from typing_extensions import Annotated

# Import the application components
from .daily_briefing_app import DailyBriefing
from .api_interactions import JSONPlaceholderClient
from .weather_client import OpenWeatherClient
from .config_reader import ConfigReader

# Create a Typer app instance. This is the main object for our CLI.
app = typer.Typer(
    help="A CLI application to generate a daily briefing for a user, including weather and recent posts.",
    add_completion=False
)

@app.command()
def get_briefing(
    #user_id: int = typer.Argument(..., help="The ID of the user to generate the briefing for."), city: str = typer.Option(..., "--city", "-c", help="The city for the weather forecast.")):
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
        # This logic is now inside the command, so it only runs when invoked.

        # Instantiate the ConfigReader, the clients, and the DailyBriefing app
        config_reader = ConfigReader()
        api_client = JSONPlaceholderClient()
        weather_client = OpenWeatherClient(config_reader=config_reader)
        # Inject dependencies into the application
        briefing_app = DailyBriefing(api_client=api_client, weather_client=weather_client)
        
        # --- Application Execution ---
        typer.echo(f"Requesting briefing for User ID: {user_id}, City: {city}...")
        briefing_message = briefing_app.generate_briefing(user_id=user_id, city=city)
        
        # --- Output ---
        if briefing_message:
            typer.secho("\n--- Your Briefing ---", fg=typer.colors.CYAN, bold=True)
            typer.echo(briefing_message)
        else:
            # This case might be hit if generate_briefing has an internal failure
            # but doesn't raise an exception.
            typer.secho("Could not generate the briefing.", fg=typer.colors.YELLOW)

    except FileNotFoundError:
        error_message = "Error: Configuration file 'config.ini' not found. Please create one based on 'config.ini.example'."
        typer.secho(error_message, fg=typer.colors.RED, err=True)
    except KeyError:
        error_message = "Error: 'api_key' for 'openweathermap' not found in config.ini. Please check your configuration."
        typer.secho(error_message, fg=typer.colors.RED, err=True)
    except Exception as e:
        # Catch-all for other unexpected errors.
        error_message = f"An unexpected application error occurred: {e}"
        typer.secho(error_message, fg=typer.colors.RED, err=True)

@app.command()
def check_config():
    """
    Checks if the configuration file is present and valid.
    """
    typer.echo("Checking for 'config.ini'...")
    try:
        ConfigReader()
        success_message = "✅ Configuration file found and seems valid."
        typer.secho(success_message, fg=typer.colors.GREEN)
    except (FileNotFoundError, KeyError) as e:
        error_message = f"❌ Configuration check failed: {e}"
        typer.secho(error_message, fg=typer.colors.RED, err=True)

# This boilerplate makes the script runnable.
if __name__ == "__main__":
    app()