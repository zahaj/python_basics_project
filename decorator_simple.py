"""
def simple_message_decorator(func):
    def wrapper_func(*args, **kwargs):
        print(f"--- Function {func.__name__} is starting ---")
        result = func(*args, *kwargs)
        print(f"--- Function {func.__name__} has finished ---")
        return result
    return wrapper_func

@simple_message_decorator
def greet(name):
    print(f"Hello, {name}!")
    return f"Greeting for {name}"

if __name__ == "__main__":
    greeting1 = greet("Alice")
    greeting2 = greet("Bob")
    print(f"Greeting from Alice: {greeting1}")
    print(f"Greeting from Bob: {greeting2}")
"""

import time

# 1. Define the decorator function
def simple_message_decorator(func):
    """
    A simple decorator that adds start/end messages around a function call.
    """
    def wrapper(*args, **kwargs):
        print(f"\n--- Starting function: '{func.__name__}' ---")
        
        # Call the original function and get its result
        result = func(*args, **kwargs)
        
        print(f"--- Finished function: '{func.__name__}' ---")
        return result
    return wrapper

# 2. Define a function and apply the decorator
@simple_message_decorator
def greet(name):
    """A simple greeting function."""
    print(f"Hello, {name}!")
    return f"Greeting completed for {name}."

# 3. Another function decorated with the same decorator
@simple_message_decorator
def calculate_sum(a, b):
    """Calculates the sum of two numbers."""
    print(f"Calculating sum of {a} and {b}...")
    time.sleep(2) # Simulate some work
    return a + b

# 1. Define the decorator function
def uppercase_output_decorator(func):
    def wrapper(*args, **xargs):
        result = func(*args, **xargs)
        if not isinstance(result, str):
            return result
        return result.upper()
    return wrapper

# 2. Define the function and apply the decorator
@uppercase_output_decorator
def get_greeting(name: str) -> str:
    return f"hello, {name}"

@uppercase_output_decorator
def get_number() -> int:
    return 666

IS_LOGGED_IN = False
def require_login_decorator(func):
    global IS_LOGGED_IN
    def wrapper(*args, **kwargs):
        if IS_LOGGED_IN:
            print(f"Access granted. Running function '{func.__name__}'")
            result = func(*args, **kwargs)
            return result
        else:
            print("Access denied. Please log in first.")
            return None
    return wrapper

@require_login_decorator
def view_private_data():
    print("Sensitive data revealed!")
    return f"Private Data"

@require_login_decorator
def post_update(message: str):
    print(f"Posting update: '{message}'")
    return f"Posted: {message}"

_api_call_count = 0
# 1. Define the decorator function
def retry(max_attempts=3, exception_to_catch=Exception):
    """
    A decorator that retries a function a specified number of times
    if it raises a given exception.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exception_to_catch as e:
                    attempts += 1
                    if attempts < max_attempts:
                        print(f"Attempt {attempts}/{max_attempts} failed for '{func.__name__}': {e}. Retrying in 1 second...")
                        time.sleep(1) # Wait before retrying
                    else:
                        print(f"All {max_attempts} attempts failed for '{func.__name__}'. Raising original exception.")
                        raise # Re-raise the last exception if all attempts fail
        return wrapper
    return decorator

# 2. Define the function and apply the decorator.
@retry(max_attempts=5, exception_to_catch=ConnectionRefusedError)
def fetch_data_from_api(url: str):
    """
    Simulates fetching data from an API that might fail a few times.
    """
    global _api_call_count
    _api_call_count += 1
    if _api_call_count <= 3: # Fail for the first 3 calls
        print(f"  (Real API call attempt {_api_call_count}: Simulating ConnectionRefusedError for {url})")
        raise ConnectionRefusedError("Failed to connect to url.")
    else:
        print(f"  (Real API call attempt {_api_call_count}: Successfully fetched data from {url})")
        return f"Data from {url}"


# Demonstrate the decorated functions
if __name__ == "__main__":
    print("--- Demonstrating Simple Decorator ---")
    
    # Call the decorated greet function
    greeting_result = greet("Alice")
    print(f"Returned from greet: {greeting_result}")

    # Call the decorated calculate_sum function
    sum_result = calculate_sum(10, 20)
    print(f"Returned from calculate_sum: {sum_result}")

    # Call the decorated get_greeting function
    get_greeting_result = get_greeting("Eva")
    print(get_greeting_result)

    get_number_result = get_number()
    print(get_number_result)

    view_private_data()
    post_update("My public post")

    IS_LOGGED_IN = True
    view_private_data()
    post_update("My public post")

    fetch_data_from_api("http://example.com/data")

        # Test: Function should succeed on the 4th attempt
    print("\n--- Test Case 1: Function eventually succeeds ---")
    try:
        data = fetch_data_from_api("http://example.com/important_data")
        print(f"Received data: {data}")
    except Exception as e:
        print(f"Caught unexpected error: {e}")

    # Reset counter for next test (important for testing multiple scenarios)
    _api_call_count = 0 
    print("\n--- Test Case 2: Function fails permanently (max_attempts too low) ---")
    @retry(max_attempts=2, exception_to_catch=ConnectionRefusedError)
    def always_fail_api(url: str):
        global _api_call_count
        _api_call_count += 1
        print(f"  (Real API call attempt {_api_call_count}: Always failing for {url})")
        raise ConnectionRefusedError(f"Always fails for {url}")

    try:
        always_fail_api("http://example.com/critical_data")
    except ConnectionRefusedError as e:
        print(f"Successfully caught expected error after retries: {e}")
    except Exception as e:
        print(f"Caught an unexpected error: {e}")