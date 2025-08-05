import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from daily_briefing.web_api import api_app, get_db

# This test doesn't require Docker to be running. It will test the API in isolation.

@pytest.fixture
def client_with_mock_db():
    """
    Fixture to create a TestClient with the database dependency mocked.
    Yields both the client and the mock session for assertions.
    """
    # --- Setup for the Mock Database ---
    # This is the mock object that our override function will yield.
    mock_db_session = MagicMock()

    # This function will replace the real get_db during the test.
    def override_get_db():
        yield mock_db_session

    # Apply the override to the app instance
    api_app.dependency_overrides[get_db] = override_get_db
    # The TestClient uses the app with the overriden dependency
    client = TestClient(api_app)

    # Yield both the client and the mock so the test can use them
    yield client, mock_db_session

    # Teardown: Clean up the override after the test is done
    api_app.dependency_overrides.clear()

# We still need to mock the clients that are created inside the endpoint.
@patch("daily_briefing.web_api.JSONPlaceholderClient")
@patch("daily_briefing.web_api.OpenWeatherClient")
def test_get_briefing_unit_success(mock_weather_client_class, mock_api_client_class, client_with_mock_db):
    """
    Unit test for the briefing endpoint using fixtures for setup.
    Mocks all external dependencies.
    """
    # Arrange
    # Unpack the tuple yielded by the fixture
    client, mock_db_session = client_with_mock_db
    # Reset the mock before each test run to ensure isolation.
    mock_db_session.reset_mock()    

    # Configure the return values for the mocked API clients.
    mock_api_client_instance = mock_api_client_class.return_value
    mock_api_client_instance.get_user.return_value = {'name': 'Test User'}
    mock_api_client_instance.get_posts_by_user.return_value = []

    # Act
    response = client.get("/briefing/99?city=Unit Test City")

    # Assert
    assert response.status_code == 200
    # Verify that the database session was used correctly
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()