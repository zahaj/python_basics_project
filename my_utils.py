def celsius_to_fahrenheit(celsius: float) -> float:
    """Converts temperature from Celsius to Fahrenheit degrees.
    
    Args:
        celsius: The temperature in degrees Celsius.
    
    Returns:
        float: The temperature in Fahreheit calculated from temperature in Celsius.
    
    Example:
    >>> celsius_to_fahrenheit(100)
    212.0
    >>> celsius_to_fahrenheit(0)
    32.0
    >>> celsius_to_fahrenheit(25)
    77.0
    """
    if not isinstance(celsius, (int, float)):
        raise TypeError("Input 'celsius' must be a number (int or float).")
    
    fahreheit = celsius * (9 / 5) + 32

    return fahreheit

def is_palindrome(text: str) -> bool:
    """Checks if a given string is a palindrome.
    
    A palindrome reads the same forwards and backwards, ignoring case,
    spaces, and punctuation.

    Arg:
        text(str): The string to be checked.

    Returns:
        bool: True if text is a palindrome, False otherwise.
    
    Example:
    >>> is_palindrome("madam")
    True
    >>> is_palindrome("Abracadabra")
    False
    >>> is_palindrome("   RacEcar  ")
    True
    """

    if not isinstance(text, str):
        raise TypeError("Input 'text' must be a string.")
    
    # Convert to lowercase and remove non-alphanumeric characters
    text_cleaned = text.lower().strip()
    
    # Check if text and reversed text are equal (palindrome definition)
    return text_cleaned == text_cleaned[::-1]  

if __name__ == "__main__":
    # This block only runs when my_utils.py is executed directly,
    # not when it's imported. Good for quick tests of the module's functions.

    import doctest # Run all of the tests from the docstring examples at once; no answer is a good answer
    doctest.testmod()

    print("--- Testing my_utils.py functions directly ---")
    print(f"0 Celsius is {celsius_to_fahrenheit(0)} Fahrenheit")
    print(f"25 Celsius is {celsius_to_fahrenheit(25)} Fahrenheit")
    print(f"100 Celsius is {celsius_to_fahrenheit(100)} Fahrenheit")

    print(f"'madam' is palindrome: {is_palindrome('madam')}")
    print(f"'hello' is palindrome: {is_palindrome('hello')}")
    print(f"'A man a plan a canal Panama' is palindrome: {is_palindrome('A man a plan a canal Panama')}")
    print(f"'Racecar!' is palindrome: {is_palindrome('Racecar!')}")