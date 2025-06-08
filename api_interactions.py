import requests
import json
from typing import List, Dict, Any, Optional

### Block 1: Introduction to Web APIs and the requests Library ###
# Practical Problem 1.1: Fetching Data from a Public API

# Define a base URL to avoid repeating it
BASE_URL = "https://jsonplaceholder.typicode.com"

def fetch_all_users() -> Optional[List[Dict[str, Any]]]:
    """
    Fetches all users from the JSONPlaceholder API.

    Returns:
        A list of user dictionaries if successful, otherwise None.
    """
    print("--- Fetching all users ---")
    url = f"{BASE_URL}/users"
    try:
        response = requests.get(url, timeout=5)  # Add a timeout for robustness
        response.raise_for_status() # Raises an HTTPError for bad responses (4XX or 5XX)
        users = response.json()
        print(f"Successfully fetched {len(users)} users.")
        print("-" * 30)
        for user in users:
            print(f"  - Name: {user.get('name')}, Email: {user.get('email')}") # use get() to prevent errors when key not found
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

def fetch_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
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

    url = f"{BASE_URL}/users/{user_id}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        user = response.json()
        # JSONPlaceholder returns an empty object {} for a non-existent ID with a 200 OK
        # A robust check is to see if the object has expected keys.
        if not user or 'id' not in user:
            print(f"User with ID {user_id} not found (API returned empty object).")
            return None
        print("Successfully fetched user.")
            
        address = user.get('address', {})
        print(f"  - Name: {user.get('name')}")
        print(f"  - Username: {user.get('username')}")
        print(f"  - Email: {user.get('email')}")
        print(f"  - City: {address.get('city')}")
        
        return user

    except requests.exceptions.HTTPError as errh:
        # A real-world API would likely return a 404 here, which raise_for_status would catch.
        print(f"HTTP Error: User with ID {user_id} not found. {errh}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Connection Error: {errc}")
    except requests.exceptions.RequestException as err:
         print(f"An unexpected error: {err}")

    return None

### Block 2: Working with API Responses & POST Requests ###
# Practical Problem 2.1: Creating a New Resource via POST

def create_new_post(title: str, body: str, user_id: int) -> Optional[Dict[str, Any]]:
    """
    Creates a new post using the JSONPlaceholder API.

    Args:
        title: The title of the post.
        body: The content of the post.
        user_id: The ID of the user creating the post.

    Returns:
        A dictionary of the created post if successful, otherwise None.
    """
    if not isinstance(user_id, int) or user_id <= 0:
        print("Error: User ID must be a positive integer.")
        return None
    if not (isinstance(title, str) or isinstance(body, str)):
        raise TypeError("A title and the body content must be strings")
    
    print(f"\n--- Creating a new post for user with ID = {user_id} ---")
    url = f"{BASE_URL}/posts"
    payload = {
        "title": title,
        "body": body,
        "userId": user_id
    }
    try:
        # The 'json' parameter automatically serializes the dict to JSON
        # and sets the 'Content-Type' header to 'application/json'.
        response = requests.post(url, json=payload, timeout=5) # Best way for JSON
        response.raise_for_status()
        # A 201 status code is the standard for successful creation
        if response.status_code == 201:
            created_post = response.json()
            print("Post created successfully.")
            print(f"  - Created Post ID: {created_post.get('id')}")
            print(f"  - Title: {created_post.get('title')}")
            return created_post
        else:
            print(f"Unexpected status code: {response.status_code}")
            return None
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: User with ID {user_id} not found. {errh}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred while creating the post: {err}")
    except TypeError as err:
         print(f"TypeError occured: {err}")
    return None

# --- Demonstration Block ---
if __name__ == "__main__":
    print("===== Running API Interaction Demonstrations =====")
    
    # Problem 1.1 Demonstration
    print(f"Trying to fetch the data for all users from URL...")
    fetch_all_users()
    print(f"Trying to fetch the data for individual users")
    fetch_user_by_id(1)
    fetch_user_by_id(5)
    print(f"Trying to fetch the data for non-existent user")
    fetch_user_by_id(999) # Test non-existent user
    print(f"Trying to fetch the data for non-valid user id")
    fetch_user_by_id(-1)  # Test invalid input

    # Problem 2.1 Demonstration
    new_post = create_new_post(
        title="This is my first post.",
        body="I'm so happy that I can post my first post!",
        user_id=1
    )
    print(f"\nNew post: {new_post}")
    print(new_post)