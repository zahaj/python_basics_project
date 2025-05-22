### Lists ###

# Problem: Creating and Accessing Lists
print(f"\n --- Creating and Accessing Lists ---")
my_list = [6, 3.1415, "Abracadabra", False, ["banana", "cherry", "apple", "strawberry"]]
print(f"List to be printed: {my_list}")
print(f"Printing...")
for item in my_list:
    print(item)
print(f"Printing finished.")
print(f"The first, the third and the last element of the list are:")
print(f"{my_list[0]}, {my_list[2]}, {my_list[-1]}.")
print(f"The slice of the list from the second to the fourth element is: {my_list[1:4]}.")

# Problem: Modifying Lists:
print(f"\n --- Modifying Lists ---")

shopping_list = ["eggs", "bread", "milk"]
print(f"Created shopping list: {shopping_list}")
shopping_list.append("cheese")
print(f"Modified list (added 'cheese' to the end of the list): {shopping_list}")
shopping_list.insert(1, "butter")
shopping_list[1] = "whole wheat bread"
print(f"Modified list ('butter' replaced with 'whole wheat butter'): {shopping_list}")
shopping_list.remove("eggs")
print(f"Modified list ('eggs' removed): {shopping_list}")
# shopping_list.remove("eggs")
if "eggs" in shopping_list: # check if the item exists in the list - avoid ValueError
    shopping_list.remove("eggs")
    print(f"After trying to remove 'chocolate' (found): {shopping_list}")
else:
    print(f"Tried to remove 'eggs', but it's not in the list. Current list: {shopping_list}")

# Problem: List Operations
print(f"\n--- List Operations ---")

numbers = [5, 2, 8, 1, 9, 3]
print(f"List of numbers: {numbers}")
print(f"""
The length of the list is {len(numbers)}.
The maximum value of the list is {max(numbers)}.
The minimum value of the list is {min(numbers)}.
The sum of all elements of the list is {sum(numbers)}.""")
numbers.sort()
print(f"The list sorted in ascending order: {numbers}. ")

more_numbers = [10, 11]
numbers.extend(more_numbers)
print(f"The list extended with {more_numbers}: {numbers}. ")

# Problem: Iterating through Lists
print(f"\n--- Iterating through Lists ---")
print(f"Printing each item in the shopping list:")
for item in shopping_list:
    print(item)
print(f"Printing each item in the shopping list with corresponding index:")
for index, item in enumerate(shopping_list):  
    print(f"{index}: {item}")


### Tuples ###
# Problem: Creating and Accessing Tuples
print(f"\n--- Creating and Accessing Tuples ---")

my_tuple = (107, "Charlie Chaplin", 2.71)
print(f"Creating a tuple: {my_tuple}")
print(f"""
The first element of the tuple is {my_tuple[0]}.
The last element of the tuple is {my_tuple[-1]}.
""")
# my_tuple[0] = "new_value" # TypeError: 'tuple' object does not support item assignment

# Problem: Tuple Operations
print(f"\n--- Tuple Operations ---")
tuple1 = (1, 2, 3)
tuple2 = (4, 5, 6)
print(f"Tuples to concatenate: tuple1: {tuple1}, tuple2: {tuple2} ")

combined_tuple = tuple1 + tuple2
print(f"Combined tuple: {combined_tuple}")
combined_tuple_length = len(combined_tuple)
print(f"Combined tuple length: {combined_tuple_length}")
print(f"The number 2 appears {combined_tuple.count(2)} times in the combined tuple.")
print(f"The number 5 has the index {combined_tuple.index(5)} in the combined tuple.")

### Dictionaries ###

# Problem: Creating and Accessing Dictionaries
print(f"\n--- Creating and Accessing Dictionaries ---")
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York",
}
print(f"Person dictionary: {person}.")
print(f"The value associated with the 'name' key is {person['name']}.")
print(f"The value associated with the 'city' key is {person['city']}.")
# Trying to access a key that doesn't exist
# This would cause KeyError if not checked: print(person["country"])

print(f"Country: {person.get('country', 'This key does not exist')}.")
# using .get() with default: person.get('country', 'Unknown')
print(f"Age: {person.get('age', 'This key does not exist')}.")
# using .get() without default: person.get('age')
#print(f"Age: {person.get('age')}.")

# Problem: Modifying Dictionaries
print(f"\n--- Modifying Dictionaries ---")
print(f"Original person dictionary: {person}")

person["occupation"] = "Engineer" # Adding a new key-value pair
print(f"After adding 'occupation': {person}.")

person["age"] = 31 # changing existing value
print(f"After changing 'age': {person}.")

del person["city"] # removing key-value pair
print(f"After removing 'city': {person}.")

# Problem: Dictionary Operations and Iteration
print(f"\n--- Dictionary Operations and Iteration ---")

scores = {"Math": 95, "Science": 88, "History": 72}
print(f"Scores dictionary: {scores}")
print(f"All keys of scores: {scores.keys()}")
print(f"All values of scores: {scores.values()}")
print(f"All key-value pairs of scores: {scores.items()}")

print("\nIterating through scores (Subject: Score):")
for subject, score in scores.items():
    print(f"Subject: {subject}, Score: {score}")

### Sets ###

# Problem: Creating and Modifying Sets
print(f"\n--- Creating and Modifying Sets ---  ")

unique_numbers = set([1, 2, 2, 3, 4, 4, 5])
print(f"Set from list with duplicates: {unique_numbers}")
unique_numbers.add(6)
print(f"After adding 6: {unique_numbers}.")
unique_numbers.add(2) # Try adding an existing element (set remains unchanged)
print(f"After trying to add 2 (no change): {unique_numbers}.")
unique_numbers.remove(4)
print(f"After removing 4: {unique_numbers}.")

# Set Operations
print(f"\n--- Set Operations ---")

set_a = {1, 2, 3, 4}
set_b = {3, 4, 5, 6}
print(f"Set A: {set_a}")
print(f"Set B: {set_b}")

print(f"The union of set A and set B (all unique elements from both): {set_a.union(set_b)}.")
print(f"The intersection of set A and set B (elements common to both): {set_a.intersection(set_b)}.")
print(f"The difference of set A and set B (elements in set_a but not in set_b): {set_a.difference(set_b)}.")
print(f"Is set A a superset of {{1, 2}}?: {set_a.issuperset({1, 2})}")

### Functions ###

# Defining a Simple Function
print(f"\n--- Defining a Simple Function ---")
def greet_user(name):
    """Prints a simple greeting to the given name."""
    print(f"Hello, {name}! Welcome.")

greet_user("Ewa")
greet_user("Christopher")

# Function with Return Value
print(f"\n--- Function with Return Value ---")
def add_numbers(a, b):
    """Return the sum of two numbers."""
    return a + b

result_1 = add_numbers(10, 5)
result_2 = add_numbers(-11, 0)
print(f"Result of adding 10 and 5: {result_1}.")
print(f"Result of adding -11 and 0: {result_2}.")

# Function with Default Arguments
print(f"\n--- Function with Default Arguments ---")
def print_message(message, sender="Unknown"):
    """Print a message with an optional sender (default value 'Unknown')."""
    print(f"{message} - From: {sender}")

print_message("Good morning!") # Uses default sender "Unknown"
print_message("See you!", "Alice") # Overrides default sender

# Function with Arbitrary Arguments (*args)
print(f"\n--- Function with Arbitrary Arguments (*args) ---")

def calculate_average(*numbers):
    """Calculate the average of any numbers of numeric arguments."""
    
    if not numbers: # checking if no numbers were passed
        return 0 # avoiding division by zero

    sum_numbers = sum(numbers)
    average = sum_numbers / len(numbers)

    return average

print(f"The average of (2, 6, 78, 3): {calculate_average(2, 6, 78, 3)}")
print(f"The average of (): {calculate_average()}") # Test with no args
print(f"The average of (0, 0, 0, 0): {calculate_average(0, 0, 0, 0)}")