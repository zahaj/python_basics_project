import os

# Set the DB_HOST environment variable for the test session.
# This MUST be done before importing any application modules that use it.
os.environ['DB_HOST'] = 'localhost'

import httpx
import pytest

from daily_briefing.database import SessionLocal, BriefingLog

def test_get_briefing_logs_to_db(setup_test_database):
    """
    Integration test: makes a real HTTP request to the running API
    and verifies that a log entry is created in the database.
    """
    # Arrange
    # Define the request parameters
    user_id = 7
    city = "IntegrationTestCity"
    api_url = f"http://127.0.0.1:8000/briefing/{user_id}?city={city}"

    # Act: Make the HTTP request to the running API.
    with httpx.Client() as client:
        response = client.get(api_url)
    
    # Assert (API Response): Check that the API call was successful.
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["user_name"] is not None # We don't care about the exact name, just that it worked.

    # Assert (Database State): Check that the correct data was written to the DB.
    with SessionLocal() as db_session: # Ensures the client is properly closed
        log_entry = db_session.query(BriefingLog).filter_by(user_id=user_id).one_or_none()
        assert log_entry is not None
        assert log_entry.user_id == user_id
        assert log_entry.city == city