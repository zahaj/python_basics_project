import requests
import json
from typing import List, Dict, Any, Optional

### Block 1: Structuring API Logic with a Client Class ###
# Practical Problem 1.1: Create a JSONPlaceholder API Client

class JSONPlaceholderClient:
    """
    A client class to interact with the JSONPlaceholder API.
    Encapsulates all API requests and error handling for this service.
    """
        
    def __init__(self, base_url: str = 'https://jsonplaceholder.typicode.com'):
        """
        Initializes the client with a base URL for the API.

        Args:
            base_url (str): The base URL for the API endpoints.
        """
        if not base_url:
            raise ValueError("Base URL cannot be empty.")        
        self.base_url = base_url

    def get_users(self) -> Optional[List[Dict[str, Any]]]:
        """
        Fetches all users from the JSONPlaceholder API.

        Returns:
            A list of user dictionaries if successful, otherwise None.
        """
        endpoint = f"{self.base_url}/users"
        print(f"Fetching all users from: {endpoint}")
        try:
            response = requests.get(endpoint, timeout=5)  # Add a timeout for robustness
            response.raise_for_status() # Raises HTTPError for bad responses (4XX or 5XX)
            users = response.json()
            print(f"Successfully fetched {len(users)} users.")
            print("-" * 30)
            # for user in users:
            #    print(f"  - Name: {user.get('name')}, Email: {user.get('email')}") # use get() to prevent errors when key not found
            return users
        except requests.exceptions.HTTPError as errh:
            print(f"Http Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Connection Error: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"An unexpected error occured: {err}")
        return None

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetches a single user by their ID from the JSONPlaceholder API.

        Args:
            user_id: The ID of the user to fetch.
        
        Returns:
            A user dictionary if successful, otherwise None.
        """
        print(f"\n--- Fetching user with ID: {user_id} ---")
        if not isinstance(user_id, int) or user_id <= 0:
            print("Error: User ID must be a positive integer.")
            return None

        endpoint = f"{self.base_url}/users/{user_id}"
        print(f"Fetching user by ID from: {endpoint}")
        try:
            response = requests.get(endpoint, timeout=5)
            response.raise_for_status()
            user = response.json()
            # JSONPlaceholder returns an empty object {} for a non-existent ID with a 200 OK
            # A robust check is to see if the object has expected keys.
            if not user or 'id' not in user:
                print(f"User with ID {user_id} not found (API returned empty object).")
                return None
            print("Successfully fetched user.")
                
            # address = user.get('address', {})
            # print(f"  - Name: {user.get('name')}")
            # print(f"  - Username: {user.get('username')}")
            # print(f"  - Email: {user.get('email')}")
            # print(f"  - City: {address.get('city')}")
            return user
        except requests.exceptions.HTTPError as errh:
            # A real-world API would likely return a 404 here, which raise_for_status would catch.
            print(f"HTTP Error: fetching user {user_id}: {errh}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Connection Error: {errc}")
        except requests.exceptions.RequestException as err:
            print(f"An unexpected error occured fetching user {user_id}: {err}")
        return None

    def create_post(self, title: str, body: str, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Creates a new post by sending data to the JSONPlaceholder API.

        Args:
            title (str): The title of the post.
            body (str): The content of the post.
            user_id (int): The ID of the user creating the post.

        Returns:
            A dictionary of the created post if successful, otherwise None.
        """
        if not isinstance(user_id, int) or user_id <= 0:
            print("Error: User ID must be a positive integer.")
            return None
        if not (isinstance(title, str) or isinstance(body, str)):
            raise TypeError("A title and the body content must be strings")
        
        endpoint = f"{self.base_url}/posts"
        payload = {
            "title": title,
            "body": body,
            "userId": user_id
        }
        print(f"Creating new post for user ID {user_id} at: {endpoint}")
        try:
            # The 'json' parameter automatically serializes the dict to JSON
            # and sets the 'Content-Type' header to 'application/json'.
            response = requests.post(endpoint, json=payload, timeout=5) # Best way for JSON
            response.raise_for_status() # Will check for 4xx and 5xx errors
            # A 201 status code is the standard for successful creation
            if response.status_code == 201:
                created_post = response.json()
                print(f"Post created successfully with status code: {response.status_code}")
                # print(f"  - Created Post ID: {created_post.get('id')}")
                # print(f"  - Title: {created_post.get('title')}")
                return created_post
            else:
                print(f"Unexpected status code: {response.status_code}")
                return None
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.RequestException as err:
            print(f"An error occurred while creating post: {err}")
        except TypeError as err:
            print(f"Type Error: {err}")
        return None

### Block 2: Handling Data Relationships and Query Parameters ###
# Practical Problem 2.1: Enhance the Client with New Methods
    def get_posts_by_user(self, user_id: int) -> Optional[List[Dict[str, Any]]]:
        """
        Fetches all posts for a specific user ID using query parameteres.
        
        Args:
            user_id (int): The ID of the user whose posts are to be fetched.

        Returns:
            A list of post dictionaries if successful, otherwise None. 
        """
        if not isinstance(user_id, int) or user_id <= 0:
            print("Error: User ID must be a positive integer.")
            return None
        
        endpoint = f"{self.base_url}/posts"
        params = {"userId": user_id}
        print(f"Fetching posts for user ID = {user_id} from: {endpoint} with params {params}")
        try:
            response = requests.get(endpoint, params=params, timeout=5)
            response.raise_for_status()
            posts = response.json()
            if posts:
                print("Posts successfully fetched.")
            else:
                print(f"No posts for user ID = {user_id}.")
            return posts
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error fetching posts for user {user_id}: {errh}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Connection Error: {errt}")
        except requests.RequestException as err:
            print(f"An unexpected errord occured fetching posts for user {user_id}: {err}")
        return None

    def get_comments_for_post(self, post_id: int) -> Optional[List[Dict[str, Any]]]:
        """
        Fetches all comments for a specific post ID.
        
        Args:
            post_id (int): The ID of the post whose comments are to be fetched.

        Returns:
            A list of comment dictionaries if successful, otherwise None. 
        """
        if not isinstance(post_id, int) or post_id <= 0:
            print("Error: Post ID must be a positive integer.")
            return None

        endpoint = f"{self.base_url}/posts/{post_id}/comments"
        print(f"Fetching comments for post {post_id} from: {endpoint}")
        try:
            response = requests.get(endpoint, timeout=5)
            response.raise_for_status()
            comments = response.json()
            print("Successfully fetched comments.")
            return comments
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Connection Error: {errc}")
        except requests.exceptions.RequestException as err:
            print(f"An error occured: {err}")
        return None
  

### Demonstration Block  ###
if __name__ == "__main__":
    print("\n===== Running Class JSONPlaceholderClient Demonstrations =====")

    # Create an instance of a JSONPlaceholderClient.
    client = JSONPlaceholderClient()
    # Call the methods on this client object to fetch all users, fetch a single user, and create a post
    client.get_users()
    client.get_user(7)
    client.create_post("My new post.", "This is awsome!", 8)

    # Fetch posts for a specific user. Print the titles of the first few posts.
    print("\n--- Posts for user with ID = 9: ---\n")
    posts_user_id_9 = client.get_posts_by_user(9)
    [print(f"- Post id: {posts_user_id_9[i]["id"]}, title: {posts_user_id_9[i]["title"]}") for i in range(5)]
    print("\n--- Posts for user with ID = 999: ---\n")
    posts_user_id_999 = client.get_posts_by_user(999)
    #[print(f"- Post id: {posts_user_id_999[i]["id"]}, title: {posts_user_id_999[i]["title"]}") for i in range(5)]

    # Fetch comments for a specific post. Print the email and body of the first few comments.
    comments_post_id_8 = client.get_comments_for_post(8)
    print("\n--- Comments for post with ID = 8: ---\n")
    [print(f"- Comment id: {comments_post_id_8[i]["id"]}\nemail: {comments_post_id_8[i]["email"]}\nbody: {comments_post_id_8[i]["body"]}") for i in range(5)]
    comments_post_id_999 = client.get_comments_for_post(999)
    print(f"\nComments for post with ID = 999: {comments_post_id_999}")