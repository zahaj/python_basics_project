"""
Unit tests for the FastAPI web application.

These tests focus on the API layer in isolation, with all external
dependencies (like the database and external API clients) mocked.
This allows for fast and reliable testing of the API's logic in isolation
without needing to run Docker or have live network connections.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from daily_briefing.web_api import api_app, get_db, get_briefing_app
from daily_briefing.models import BriefingResponse

@pytest.fixture
def client_with_mock_deps():
    """
    Pytest fixture to create a FastAPI TestClient with mocked dependencies.

    This fixture uses FastAPI's dependency override mechanism to replace the
    real `get_db` dependency and application logic with mock objects.
    This allows us to test fast the API endpoint's interaction with the database
    (e.g., that it calls `db.add()` and `db.commit()`) without needing a real
    database connection.

    Yields:
        tuple: A tuple containing the configured TestClient, the mock DB session
        and the mock briefing app.
    """
    mock_db_session = MagicMock()
    mock_briefing_app = MagicMock()

    def override_get_db():
        """A dependency override that yields the mock session."""
        yield mock_db_session

    def override_get_briefing_app():
        yield mock_briefing_app

    api_app.dependency_overrides[get_db] = override_get_db
    api_app.dependency_overrides[get_briefing_app] = override_get_briefing_app

    client = TestClient(api_app)
    yield client, mock_db_session, mock_briefing_app

    # Teardown: Clean up the override after the test is done
    api_app.dependency_overrides.clear()

def test_get_briefing_unit_success(client_with_mock_deps):
    """
    Tests a successful request to the /briefing/{user_id} endpoint.

    This test verifies that the endpoint correctly calls the application logic,
    logs the event to the database, and returns a successful response. It mocks
    the briefing application and the database to ensure the test is isolated.
    """
    # Arrange
    # Unpack the client and mock db_session yielded from the fixture
    client, mock_db_session, mock_briefing_app = client_with_mock_deps
    mock_db_session.reset_mock()
    mock_briefing_app.reset_mock()  

    # Configure the mock briefing app to return a dummy response
    mock_briefing_app.generate_briefing_for_api.return_value = BriefingResponse(
        user_name="Mock User",
        city="Mock City",
        weather_summary="Always sunny",
        latest_post_title="Mock Post"
    )

    # Act
    response = client.get("/briefing/99?city=Mock City")

    # Assert
    # 1. Assert that the API returned a successful status code.
    assert response.status_code == 200
    assert response.json()["user_name"] == "Mock User"
    # 2. Assert that the application logic was called correctly.
    mock_briefing_app.generate_briefing_for_api.assert_called_once_with(
        user_id=99, city="Mock City"
    )
    # 3. Assert that a log entry was added and committed to the database.
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()