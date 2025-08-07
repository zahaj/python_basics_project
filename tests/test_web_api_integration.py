import os

# Set the DB_HOST environment variable for the test session.
# This MUST be done before importing any application modules that use it.
os.environ['DB_HOST'] = 'localhost'

import httpx
import pytest

from daily_briefing.database import SessionLocal, BriefingLog

def test_get_briefing_logs_to_db(db_session_setup):
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

def test_get_and_delete_logs_from_db(db_session_setup):
    """
    Tests the full lifecycle: creating a log, reading it, deleting it,
    and verifying it's gone.
    """

    # Arrange: Create a log entry first by calling the original endpoint
    httpx.get("http://127.0.0.1:8000/briefing/10?city=DeleteTest")

    # Act & Assert 1: Get all logs and verify the new entry is present
    response_get = httpx.get("http://127.0.0.1:8000/logs")
    assert response_get.status_code == 200
    logs = response_get.json()
    assert isinstance(logs, list)
    assert len(logs) > 0

    # Find the log we just created
    test_log = next((log for log in logs if log["city"] == "DeleteTest"), None)
    assert test_log is not None
    log_id_to_delete = test_log["id"]

    # Act & Assert 2: Delete the log
    response_delete = httpx.delete(f"http://127.0.0.1:8000/logs/{log_id_to_delete}")
    assert response_delete.status_code == 200
 
    # Act & Assert 3: Verify the log is gone
    response_get_again = httpx.get(f"http://127.0.0.1:8000/logs/{log_id_to_delete}")
    response_get_again.status_code == 404