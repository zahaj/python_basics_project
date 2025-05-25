### Modules ###

import math
import random
from typing import List, Union, Any
# Optional[str] is a shorthand for Union[str, None].


# --- Import our custom utility module ---
# Make sure my_utils.py is in the same directory or accessible via PYTHONPATH

import my_utils

# 2. Import and Use Your Module
print("\n--- Using my_utils module ---")

try:
    print(f"Temperature 0 celsius is equal to {my_utils.celsius_to_fahrenheit(0)}.")
    print(f"Temperature 25 celsius is equal to {my_utils.celsius_to_fahrenheit(25)}.")
    print(f"Temperature 100 celsius is equal to {my_utils.celsius_to_fahrenheit(100)}.")

    print(f"Is 'madam' a palindrome? {my_utils.is_palindrome('madam')}")
    print(f"Is 'hello' a palindrome? {my_utils.is_palindrome('hello')}")
    print(f"Is 'A man a plan a canal Panama' a palindrome? {my_utils.is_palindrome('A man a plan a canal Panama')}")

except (TypeError, ValueError) as e:
    print(f"Error using my_utils functions: {e}")

# 3. Explore Built-in Modules
print("\n--- Exploring Built-in Modules (math, random) ---")

print(f"The square root of 25 is {math.sqrt(25)}.")
print(f"The value of pi is {math.pi}.")

print(f"A random integer between 1 and 100 (inclusive): {random.randint(1, 100)}")
print(f"A random float between 0.0 and 0.1 (exclusive): {random.random()}")

### Error Handling (try, except, finally) ###

# 1. Handling ValueError (for invalid input)
print(f"\n--- Handling ValueError for invalid input ---")

number_str = input("Enter a number: ")
try:
    number = int(number_str)
    print(f"You entered {number}.")
except ValueError:
    print(f"Error: Invalid input. Please enter a valid number.")

# 2. Handling ZeroDivisionError
print(f"\n--- Handling ZeroDivisionError ---")

try:
    numerator_str = input("Enter a numerator: ")
    denominator_str = input("Enter a denominator: ")
    numerator = float(numerator_str) # Use float to allow decimal numbers
    denominator = float(denominator_str)

    result = numerator / denominator
    print(f"{numerator_str} divided by {denominator_str} equals to {result}.")
except ValueError:
    print("Error: Invalid input. Please ensure both numerator and denominator are valid numbers.")
except ZeroDivisionError:
    print("Error: Cannot divide by zero.")

# 3. Handling Multiple Specific Exceptions
print("\n--- Handling Multiple Specific Exceptions ---")

def get_list_element(my_list: List[Any], index: Union[int, float]) -> Any:
    """Attempts to return an element from a list at a given index.

    Handles IndexError if index is out of bounds and TypeError if inputs
    are not of the expected types.
    
    Args:
        my_list(List[Any]): The list from which to retrieve an element.
        index(Union[int, float): The index of the element to retrieve.

    Returns:
        Any: The element at the specified index, or None if an error occurs.
    
    Examples:
    >>> get_list_element([1, 6, 8, "apple"], 3)
    apple
    >>> get_list_element([[1, 0, 86], 6, 8, "apple"], 0)
    [1, 0, 86]
    >>> get_list_element([], 0)
    """
    
    try:
        # Check if index is an integer first, as float index isn't valid for list access
        if not isinstance(index, int):
            raise TypeError("Index must be an integer.")
        return my_list[index]
    except IndexError:
        print("Error: Index is out of bounds.")
        return None
    except TypeError as e:
        # Catch TypeError if my_list is not a list or index is not numeric
        print(f"Error: Invalid type provided for list or index: {e}. Ensure list is a list and index is an integer.")
        return None
    except Exception as e: # General catch-all for any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return None

test_list = [10, 89, "Bamboo", 3.89, 0, True]
print(f"The list for testing: {test_list}.")
print(f"Element of the list at index 2: {get_list_element(test_list, 2)}") # Valid list and index
print(f"Element of the list at index -1: {get_list_element(test_list, -1)}") # Valid list and index
print(f"Element of the list at index 10: {get_list_element(test_list, 10)}") # IndexError
print(f"Element from a string: {get_list_element('New York', -1)}") # TypeError (list)
print(f"Element with string index: {get_list_element(test_list, 'Bobby')}") # TypeError (index)

# 4. Using finally
print("\n--- Using finally  Block ---")
file_name_for_finally = "non_existent_file_for_test.txt"

try:
    print(f"Attempting to open '{file_name_for_finally}'...")
    with open(file_name_for_finally, "r") as f:
        content = f.read()
        print(f"File content: {content[:50]}...") # Print first 50 chars if successful
except FileNotFoundError:
    print(f"Error: The file {file_name_for_finally} was not found.")
except Exception as e:
    print(f"An unexpected error occurred during file operation: {e}")
finally:
# This block always executes, whether an error occurred or not.
    # It's crucial for cleanup operations like closing files, releasing resources, etc.
    print("Attempted file operation complete. Cleanup actions would go here.")

### File Input/Output (I/O) ###

# 1. Writing to a File
print("\n--- Writing to a File ---")
lines_to_write = ["First line.", "Second line.", "Third line."]
file_to_write = "my_output.txt"

# Old way of writing to a file with explicitly closing a file.
file_to_write_old = "my_output_old.txt"
try:
    output_file = open(file_to_write_old, "w")
    for line in lines_to_write:
        output_file.write(line + "\n")
    print(f"Content written to '{file_to_write_old}' (old way).")
except IOError as e:
    print(f"Error writing file (old way): {e}")
finally:
    if output_file:
        output_file.close()
        print(f"File '{file_to_write_old}' closed (old way).")

# 2. Reading from a File
print("\n--- Reading from a File ---")
   
try:
    file_to_read_old = open(file_to_write_old, "r")
    print(f"Reading a file '{file_to_write_old}'...")
    for line in file_to_read_old:
        print(line.strip())
except Exception as e:
    print(f"Something went wrong: {e}.")
finally:
    if file_to_read_old:
        file_to_read_old.close()
        print(f"File '{file_to_write_old}' closed.")

# 3. Appending to a File (using 'a' mode)
print("\n--- Appending to a File ---")
new_line_to_append = "This is an appended line."

file_object = None  # Initialize file_object to None
try:
    print(f"Opening a File '{file_to_write_old}' in 'a' mode... Pointer at the end of a file.")
    file_object = open(file_to_write_old, "a")
    print(f"Appending a line '{new_line_to_append}'.")
    file_object.write(new_line_to_append)
    print("New line appended successfully.")
except OSError as e:
    print(f"Error writing to file: {e}")
finally:
    if file_object:
        file_object.close()
        print("File closed after appending.")

file_object = None  # Reset file_object for the next operation
try:
    # Verify by reading again
    file_object = open(file_to_write_old, "r")
    content = file_object.read()
    print("\nContent after appending:")
    print(content)
except FileNotFoundError:
    print(f"Error: '{file_to_write_old}' not found for reading.")
except IOError as e:
# Code to execute if an IOError occurs
    print(f"Error reading file. An I/O error occurred: {e}")
    # You can also get more specific details from the error object:
    # print(f"Error number: {e.errno}")
    # print(f"Error message: {e.strerror}")
    # print(f"File path: {e.filename}")
finally:
    if file_object:
        file_object.close()
        print(f"File '{file_to_write_old}' closed after reading.")

# 4. Using with open() (The Pythonic Way) which ensures that a file is closed.

print("\n--- The 'with open()' Statement ---")
print("As demonstrated below, `with open()` automatically handles file closing,")
print("even if errors occur within the block. This prevents resource leaks and is safer.")
print("It's highly recommended over explicit open()/close() calls.")

# Writing
print("\nWriting to a file")
try:
    print(f"Writing {lines_to_write} to a file '{file_to_write}'...")
    with open(file_to_write, "w") as f:
        for line in lines_to_write:
            f.write(line + "\n")
except IOError as e: # (IOError, OSError)
# OSError is the more encompassing and modern exception to catch in Python 3 for I/O related issues.
# IOError is now effectively an alias for OSError in Python 3, meaning if you catch IOError, you are
#  also catching OSError. But it's better to explicitly catch the more general OSError if you want to
# cover all potential operating system-related errors that might occur during file operations.
    print(f"Error writing file: {e}")

# Reading
try:
    with open(file_to_write, "r") as f:
        # content_file_to_write = f.read()
        # print(content_file_to_write.strip()) # Remove newline characters if the file ends with one        
        print(f"\nReading from a file '{file_to_write}' line by line:")
        for i, line in enumerate(f):
            print(f"Line {i+1}: {line.strip()}")
except FileNotFoundError:
    print(f"Error: '{file_to_write}' not found for reading.")
except IOError as e:
    print(f"Error reading file: {e}")

# Appending
try:
    print(f"\nAppending '{new_line_to_append}' to a file '{file_to_write}'...")
    with open(file_to_write, "a") as f:
        f.write(new_line_to_append)
    # Verify by reading again
    with open(file_to_write, "r") as f:
        print("Content after appending:")
        print(f.read())
except FileNotFoundError:
    print(f"Error: '{file_to_write}' not found for reading.")
except IOError as e:
    print(f"Error reading file: {e}")

# 5. Reading from and Writing to a CSV-like File (Simple Parsing):

# First, ensure you have a data.csv file in the same directory:
# Name,Age,City
# Alice,30,New York
# Bob,24,London
# Charlie,35,Paris

print(f"\n--- Reading from and Writing to a CSV-like File (Simple Parsing) ---")

csv_file_name = "data.csv"
processed_people_data = [] # To store dictionaries of processed data

try:
    with open(csv_file_name, "r") as csv_file:
        header = csv_file.readline().strip().split(',') # Read and split header into list
        print(f"CSV Header: {header}")
    
        for line_number, line in enumerate(csv_file): # Process all lines after header
            line_list = line.strip().split(",") # list for items in a data line (e.g. Alice,30,New York)
            if len(line_list) == len(header): # Basic validation for lines with complete data set
                print(f"{line_list[0]} is {line_list[1]} years old.")
                person_dict = {}
                for i in range(len(header)):
                    person_dict[header[i]] = line_list[i]
                processed_people_data.append(person_dict)
            else:
                print(f"Warning: Skipping malformed line {line_number + 1}: {line.strip()}")

    # Write Processed Data (Optional Challenge)
    processed_data_filename = "processed_data.txt"
    
    with open(processed_data_filename, "w") as output_file:
        output_file.write("Processed People Data:\n")
        for person_dict in processed_people_data:
            # alternatively get keys using {person_dict.get('Name', 'N/A')}
            output_file.write(f"Name: {person_dict['Name']}, Age: {person_dict['Age']}, City: {person_dict['City']}\n")
        print(f"Processed data written to '{processed_data_filename}'.")

except FileNotFoundError:
    print(f"Error: CSV file '{csv_file_name}' not found. Please create it manually.")
except IOError as e:
    print(f"Error reading/writing CSV file: {e}")
except Exception as e:
    print(f"An unexpected error occurred during CSV processing: {e}")