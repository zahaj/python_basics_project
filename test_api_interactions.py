import unittest
from unittest.mock import patch, MagicMock
import requests.exceptions

from api_interactions import JSONPlaceholderClient

class TestJSONPlaceholderClient(unittest.TestCase):
    """Test suite for JSONPlaceholderClient class."""

    def setUp(self):
        """Set up a client instance for each test."""

        self.client = JSONPlaceholderClient()
    
    @patch("api_interactions.requests.get")
    def test_get_users_success(self, mock_requests_get):
        """Test successful fetching of all users."""

        # Arrange
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = MagicMock()
        mock_response.status_code = 200
        users = [
            {"id": 1, "name": "Leanne Graham", "email": "Sincere@april.biz"},
            {"id": 2, "name": "Ervin Howell", "email": "Shanna@melissa.tv"}
        ]
        mock_response.json.return_value = users
        mock_requests_get.return_value = mock_response
        # print(type(self.client), dir(self.client))

        # Act
        result = self.client.get_users()
        
        # Assert
        mock_response.json.assert_called_once()
        mock_requests_get.assert_called_once_with(f"{self.client.base_url}/users", timeout=5)
        self.assertEqual(result, users)

    @patch("api_interactions.requests.get")
    def test_get_users_failure(self, mock_requests_get):
        """Test failure when fetching all users."""

        # Arrange
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error: Not Found")
        mock_requests_get.status_code = 404
        mock_requests_get.return_value = mock_response
        # Act
        result = self.client.get_users()
        
        # Assert
        mock_requests_get.assert_called_once_with("https://jsonplaceholder.typicode.com/users", timeout=5)
        self.assertIsNone(result)

    @patch("api_interactions.requests.get")
    def test_get_posts_by_user_success(self, mock_requests_get):
        """Test successful fetching of posts for a specific user."""

        # Arrange
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = MagicMock()
        mock_response.status_code = 200
        posts = [
            {'userId': 9, 'id': 81, 'title': 'tempora rem veritatis voluptas', 'body': 'facere qui nesciunt est voluptatum'},
            {'userId': 9, 'id': 82, 'title': 'laudantium voluptate suscipit', 'body': 'ut libero sit aut totam inventore sunt'},
            {'userId': 9, 'id': 83, 'title': 'odit et voluptates doloribus', 'body': 'est molestiae facilis quis tempora'}
        ]
        mock_response.json.return_value = posts
        mock_requests_get.return_value = mock_response

        # Act
        result = self.client.get_posts_by_user(user_id=1)

        # Assert
        expected_params = {"userId": 1}
        mock_requests_get.assert_called_once_with(f"{self.client.base_url}/posts", params=expected_params, timeout=5)
        self.assertEqual(result, posts)

    @patch("api_interactions.requests.post")
    def test_create_post_success(self, mock_requests_post):
        """Test successful creation of a new post."""

        # Arrange
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = MagicMock()
        mock_response.status_code = 201
        post = {
            "title": "Test title",
            "body": "Test body",
            "userId": 4,
            "id": 105}
        mock_response.json.return_value = post
        mock_requests_post.return_value = mock_response

        # Act
        post_payload = {
            "title": "Test title",
            "body": "Test body",
            "userId": 4
        }
        result = self.client.create_post(
            title=post_payload['title'],
            body=post_payload['body'],
            user_id=post_payload['userId']
        )

        # Assert
        mock_requests_post.assert_called_once_with(f"{self.client.base_url}/posts", json=post_payload, timeout=5)
        mock_response.json.assert_called_once()
        self.assertEqual(result, post)