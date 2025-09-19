"""
Client for interacting with the JSONPlaceholder public API.

This module encapsulates all the logic for making HTTP requests to the
JSONPlaceholder service, handling responses, and managing errors.
"""
import logging
from typing import List, Dict, Any, Optional

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class JSONPlaceholderClient:
    """A client class for the JSONPlaceholder API."""
        
    def __init__(self, base_url: str = 'https://jsonplaceholder.typicode.com'):
        """
        Initializes the client with the API's base URL.

        Args:
            base_url (str): The base URL for the API endpoints.
        """
        if not base_url:
            raise ValueError("Base URL cannot be empty.")        
        self.base_url = base_url

    def get_users(self) -> Optional[List[Dict[str, Any]]]:
        """
        Fetches all users from the API.

        Returns:
            A list of user dictionaries if successful, otherwise None.
        """
        logging.info(f"Fetching all users from: {self.base_url}/users")
        try:
            response = requests.get(f"{self.base_url}/users", timeout=5)
            response.raise_for_status()
            users = response.json()
            logging.info(f"Successfully fetched {len(users)} users.")
            return users
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred fetching users: {e}")
        return None

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetches a single user by their ID from the API.

        Args:
            user_id: The ID of the user to fetch.
        
        Returns:
            A user dictionary if successful, otherwise None.
        """
        logging.info(f"Fetching user by ID: {user_id} from: {self.base_url}/users/{user_id}")
        if not isinstance(user_id, int) or user_id <= 0:
            logging.error("User ID must be a positive integer.")
            return None

        try:
            response = requests.get(f"{self.base_url}/users/{user_id}", timeout=5)
            response.raise_for_status()
            user = response.json()
            # JSONPlaceholder returns an empty object {} for a non-existent ID with a 200 OK
            # A robust check is to see if the object has expected keys.
            if not user or 'id' not in user:
                logging.warning(f"User with ID {user_id} not found (API returned empty object).")
                return None
            logging.info(f"Successfully fetched user with ID {user_id}.")
            return user
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred fetching user {user_id}: {e}")
        return None

    def create_post(self, title: str, body: str, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Creates a new post for a given user.

        Args:
            title (str): The title of the post.
            body (str): The content of the post.
            user_id (int): The ID of the user creating the post.

        Returns:
            A dictionary of the created post if successful, otherwise None.
        """
        logging.info(f"Creating new post for user ID {user_id} at {self.base_url}/posts")
        if not isinstance(user_id, int) or user_id <= 0:
            logging.error("User ID must be a positive integer.")
            return None
        if not isinstance(title, str):
            raise TypeError("Post's title must be a string")
        if not isinstance(body, str):
            raise TypeError("Post's body must be a string")

        payload = {
            "title": title,
            "body": body,
            "userId": user_id
        }
        try:
            response = requests.post(f"{self.base_url}/posts", json=payload, timeout=5)
            response.raise_for_status()
            if response.status_code == 201:
                created_post = response.json()
                logging.info(f"Post created successfully with ID: {created_post.get('id')}")
                return created_post
            else:
                logging.warning(f"Post creation returned unexpected status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred while creating post: {e}")
        except TypeError as err:
            logging.error(f"Invalid post data: {err}")
        return None

    def get_posts_by_user(self, user_id: int) -> Optional[List[Dict[str, Any]]]:
        """
        Fetches all posts for a specific user ID using query parameteres.
        
        Args:
            user_id (int): The ID of the user whose posts are to be fetched.

        Returns:
            A list of post dictionaries if successful, otherwise None. 
        """
        logging.info(f"Fetching posts for user ID {user_id} from: {self.base_url}/posts...")
        if not isinstance(user_id, int) or user_id <= 0:
            logging.error("User ID must be a positive integer.")
            return None

        params = {"userId": user_id}        
        try:
            response = requests.get(f"{self.base_url}/posts", params=params, timeout=5)
            response.raise_for_status()
            posts = response.json()
            if posts:
                logging.info(f"Successfully fetched {len(posts)} posts for user {user_id}.")
                return posts
            else:
                logging.info(f"No posts for user ID: {user_id}.")
        except requests.RequestException as e:
            logging.error(f"An error occurred fetching posts for user {user_id}: {e}")
        return None

    def get_comments_for_post(self, post_id: int) -> Optional[List[Dict[str, Any]]]:
        """
        Fetches all comments for a specific post ID.
        
        Args:
            post_id (int): The ID of the post whose comments are to be fetched.

        Returns:
            A list of comment dictionaries if successful, otherwise None. 
        """
        logging.info(f"Fetching comments for post {post_id} at {self.base_url}/posts/{post_id}/comments...")
        if not isinstance(post_id, int) or post_id <= 0:
            logging.error("Post ID must be a positive integer.")
            return None

        try:
            response = requests.get(f"{self.base_url}/posts/{post_id}/comments", timeout=5)
            response.raise_for_status()
            comments = response.json()
            if comments:
                logging.info(f"Successfully fetched {len(comments)} comments for post {post_id}.")
                return comments
            else:
                logging.info(f"No comments for post {post_id}.")
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred fetching comments for post {post_id}: {e}")
        return None