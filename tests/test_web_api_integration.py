import httpx
import pytest

from daily_briefing.database import SessionLocal, BriefingLog
from daily_briefing.auth import get_password_hash

def get_auth_token():
    """Helper function to get an authentication token."""
    response = httpx.post(
        "http://127.0.0.1:8000/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    response.raise_for_status()
    print(f"Respons from get_auth_token:{response}\n response.json: {response.json()}")
    return response.json()["access_token"]

def test_get_briefing_logs_unauthorized(db_session_setup):
    """
    Integration test: makes a real HTTP request to the running API
    and verifies that accessing a protected endpoint without a token fails.
    """
    with httpx.Client() as client:
        response = client.get("http://127.0.0.1:8000/logs")
    assert response.status_code == 401

def test_get_and_delete_logs_authorized(db_session_setup):
    """
    Tests the full authorized lifecycle: getting a token, creating a log,
    reading it, deleting it, and verifying it's gone.
    """
    # Arrange: Get an auth token first
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    with httpx.Client(headers=headers) as client:
        # Act 1: Create a log entry by calling the original endpoint
        # The /briefing endpoint is not protected, so it doesn't need auth
        user_id = 7
        city = "IntegrationTestCity"
        api_url = f"http://127.0.0.1:8000/briefing/{user_id}?city={city}"
        httpx.get(api_url)

        # Act & Assert 2: Get all logs and verify the new entry is present
        response_get_all_logs = client.get("http://127.0.0.1:8000/logs")
        assert response_get_all_logs.status_code == 200
        logs = response_get_all_logs.json()
        test_log = next((log for log in logs if log["city"] == "IntegrationTestCity"), None)
        assert test_log is not None
        log_id_to_delete = test_log["id"]

        # Act and Assert 3: Delete the log
        response_delete_log = client.delete(f"http://127.0.0.1:8000/logs/{log_id_to_delete}")
        assert response_delete_log.status_code == 200

        # Act & Assert 4: Verify the log is gone by trying to get it by ID
        response_get_log_again = client.get(f"http://127.0.0.1:8000/logs/{log_id_to_delete}")
        assert response_get_log_again.status_code == 404