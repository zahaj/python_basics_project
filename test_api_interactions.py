import unittest
from unittest.mock import patch, MagicMock
import requests.exceptions

from api_interactions import (
    fetch_all_users,
    fetch_user_by_id,
    create_new_post
)

# Block 3: Advanced Error Handling and Testing API Interactions

class TestFetchUsers(unittest.TestCase):
    """
    Test suite for fetch functions in api_interactions.py.
    """

    @patch('api_interactions.requests.get')
    def test_fetch_all_users_success(self, mock_requests_get):
        """Test fetch_all_users returns user list on a successful API call."""

        # Arrange: Configure the mock to simulate a successful API response.
        # 1. Create the stunt double for the Response object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        # Simulate .json()
        users = [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'}
        ]
        mock_response.json.return_value = users
        # mock_response.text = "Some text" # Simulate .text

        mock_requests_get.return_value = mock_response
        result = fetch_all_users()

        mock_requests_get.assert_called_once_with("https://jsonplaceholder.typicode.com/users", timeout=5)
        self.assertEqual(result, users)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'Alice')

    @patch('api_interactions.requests.get')
    def test_fetch_all_users_http_error(self, mock_requests_get):
        """Test fetch_all_users returns None when an HTTPError occurs."""

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error: Not Found")
        mock_requests_get.status_code = 404
        mock_requests_get.return_value = mock_response

        result = fetch_all_users()

        mock_requests_get.assert_called_once_with("https://jsonplaceholder.typicode.com/users", timeout=5)
        mock_response.raise_for_status.assert_called_once()
        self.assertIsNone(result)

    @patch('api_interactions.requests.get')
    def test_fetch_user_by_id_success(self, mock_requests_get):
        """Test fetch_user_by_id returns a user on a successful API call."""
        # Arrange
        user_id = 5
        mock_response  = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock() # This is just a dummy Mock object if not configured and called
        # When raise_for_status() is called on a response mock, it doesn't raise anything — it just "swallows" the call
        # because it's a mock's default behaviour 
        
        user = {
            'id': user_id,
            'name': 'Clementina DuBuque',
            'username': 'Moriah.Stanton',
        }
        mock_response.json.return_value = user
        mock_requests_get.return_value = mock_response
        
        # Act
        result = fetch_user_by_id(user_id)

        # Assert
        mock_requests_get.assert_called_once_with(f"https://jsonplaceholder.typicode.com/users/{user_id}", timeout=5)
        self.assertEqual(result, user)
        self.assertIsNotNone(user)


    @patch('api_interactions.requests.get')
    def test_fetch_user_by_id_not_found(self, mock_requests_get):
        """Test fetch_user_by_id function returns None when an HTTPError occurs."""
        # Arrange
        user_id = 999
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
        mock_requests_get.return_value = mock_response

        # Act
        result = fetch_user_by_id(user_id)

        # Assert
        mock_response.raise_for_status.assert_called_once()
        self.assertIsNone(result)

class TestCreatePost(unittest.TestCase):
    """Test Suite for create_new_post function in api_interactions.py."""

    @patch('api_interactions.requests.post')
    def test_create_new_post_success(self, mock_requests_post):
        """Test create_new_post returns a new post on a successful API call."""        
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.raise_for_status.return_value = MagicMock()
        mock_response.json.return_value = {"title": "Test Title", "body": "Test Body", "userId": 25, "id": 152}  # Simulate API response
        mock_requests_post.return_value = mock_response

        # Act
        result = create_new_post("Test Title", "Test Body", 25)
        # Assert
        mock_requests_post.assert_called_once_with("https://jsonplaceholder.typicode.com/posts", json={"title": "Test Title", "body": "Test Body", 'userId': 25}, timeout=5)
        self.assertEqual(result, {"title": "Test Title", "body": "Test Body", "userId": 25, "id": 152})
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], 152)
        self.assertEqual(result["title"], "Test Title")

    @patch('api_interactions.requests.post')    
    def test_create_new_post_error_404(self, mock_requests_post):
        """Test create_new_post returns None when an HTTPError occurs."""
        # Arrange
        mock_response = MagicMock()
        #mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
        mock_response.status_code = 404
        mock_requests_post.return_value = mock_response

        # Act
        result = create_new_post("Test Title", "Test Body", 25)

        # Assert
        mock_requests_post.assert_called_once_with("https://jsonplaceholder.typicode.com/posts", json={"title": "Test Title", "body": "Test Body", 'userId': 25}, timeout=5)
        mock_response.raise_for_status.assert_called_once()
        self.assertIsNone(result)
    
    @patch('api_interactions.requests.post')    
    def test_create_new_post_connection_error(self, mock_requests_post):
        """Test create_new_post returns None when a ConnectionError occurs."""
        # Arrange
        mock_requests_post.side_effect = requests.exceptions.ConnectionError("Failed to connect")

        # Act
        result = create_new_post("Test Title", "Test Body", 25)

        # Assert
        mock_requests_post.assert_called_once_with("https://jsonplaceholder.typicode.com/posts", json={"title": "Test Title", "body": "Test Body", 'userId': 25}, timeout=5)
        self.assertIsNone(result)