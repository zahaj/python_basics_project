"""
Integration tests for the Daily Briefing API.

These tests run against a live application and database, verifying the
end-to-end functionality of the API endpoints.
"""
import httpx

from daily_briefing.database import BriefingLog
from conftest import TestingSessionLocal

def get_auth_token() -> str:
    """
    Helper function to authenticate and retrieve a JWT access token.

    This function simulates a client logging in to the /token endpoint
    to get a token that can be used to access protected resources.

    Returns:
        The access token as a string.
    """
    response = httpx.post(
        "http://127.0.0.1:8000/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    response.raise_for_status()
    return response.json()["access_token"]

def test_unauthorized_access_to_protected_endpoint(db_session_setup):
    """
    Verifies that accessing a protected endpoint without a token
    correctly results in a 401 Unauthorized error.
    """
    # Arrange & Act
    # Make a request to a protected endpoint without an Authorization header.
    with httpx.Client() as client:
        response = client.get("http://127.0.0.1:8000/logs")
    assert response.status_code == 401, "Should return 401 Unauthorized"

def test_authorized_log_creation_and_deletion(db_session_setup):
    """
    Tests the full authorized lifecycle of a log entry:
    1. A log is implicitly created by calling the (unprotected) /briefing endpoint.
    2. The test authenticates, gets a token, and uses it to...
    3. Fetch all logs and verify the new entry exists.
    4. Delete the newly created log.
    5. Verify that the log is gone.
    """
    # Arrange
    # 1. Get an authentication token
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create a log entry directly in the database for a reliable setup.
    # This endpoint is not protected and serves to populate our database.
    db = TestingSessionLocal()
    new_log = BriefingLog(user_id=99, city="IntegrationTestCity")
    db.add(new_log)
    db.commit()
    log_id_to_delete = new_log.id
    db.close()

    # Act & Assert
    # Use a client with the authorization headers for all subsequent requests.
    with httpx.Client(headers=headers) as client:
        # 3. Fetch all logs and find the one we just created.
        response_get = client.get("http://127.0.0.1:8000/logs")
        assert response_get.status_code == 200
        logs = response_get.json()
        test_log = next((log for log in logs if log["id"] == log_id_to_delete), None)

        assert test_log is not None, "Test log not found via API"
        assert test_log["city"] == "IntegrationTestCity"

        # 4. Delete the log.
        response_delete = client.delete(f"http://127.0.0.1:8000/logs/{log_id_to_delete}")
        assert response_delete.status_code == 204

        # 5. Verify the log is truly gone by trying to fetch it by its ID.
        response_get_again = client.get(f"http://127.0.0.1:8000/logs/{log_id_to_delete}")
        assert response_get_again.status_code == 404, "Log should not be found after deletion"