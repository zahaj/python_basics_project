# Problem: Counting Up to 10
print(f"\n --- Counting Up to 10 ---")

for i in range(0, 11):
    print(i)

print(f"Counting Up finished.")

# Problem: Iterating Over a List of Fruits
print(f"\n--- Iterating Over a List of Fruits ---")
fruits = ["apple", "banana", "cherry", "date"]
print(f"Iterating list {fruits}:")
for fruit in fruits:
    print(fruit)

print(f"Iterating finished.")

# Problem: Summing Numbers in a List
print(f"\n --- Summing Numbers in a List ---")
numbers = [10, 20, 30, 40, 50]
print(f"Summing numbers in a list {numbers}.")

total_sum = 0
for number in numbers:
    total_sum += number

print(f"The sum of {numbers} is {total_sum}, {sum(numbers)}.")

# Problem: Counting Vowels in a Word entered by a user
# For checking if an item is in a collection, Python's set data structure is typically
# the fastest for larger collections due to its optimized hash-based lookups.

print(f"\n --- Count Vowels in a Word ---")

word = input("Enter a word for counting vowels: ")
vowel_count = 0
vowels = "aeiouyAEIOUY"
for letter in word:
    if letter in vowels:
        vowel_count += 1

print(f"There are {vowel_count} vowels in word '{word}'. ")

# Problem: Simple countdown with while loop
print(f"\n --- Simple Countdown ---")
print(f"Counting down from 5 to 1...")

count = 5
while count > 0:
    print(count)
    count -= 1
print("Lift off!")
print(f"Countdown finished.")

# Problem: User Input Loop (Sentinel Value)
print("\n--- User Input Loop ---")
print("Enter words, or type 'quit' to exit.")

while True: # This creates an infinite loop
    user_word = input("Enter a word: ")

    if user_word.lower() == "quit": # Convert to lowercase to handle "Quit", "QUIT", etc.
        print("Exiting word input program.")
        break
    else:
        print(f"You entered: {user_word}")

print("User Input Loop finished.\n")

# --- Problem: Basic Menu System ---
print("\n--- Basic Menu System ---")
while True:
    print(f"""Menu:
    1. Say Hello
    2. Say Goodbye
    3. Exit
    """)

    user_choice = input("Enter your choice (1, 2, or 3): ")
    
    if user_choice == "1":
        print("Hello!")
    elif user_choice == "2":
        print("Goodbye!")
    elif user_choice == "3":
        print("Exiting...")
        break
    else:
        print("Invalid option. Please try again, choose 1, 2, or 3.")

print("Menu System finished.\n")

# --- Problem: Finding the First Even Number ---
print("\n--- Finding the First Even Number ---")

numbers1 = [1, 3, 5, 8, 7, 9, 10, 12]
numbers2 = [1, 3, 5, 7, 9] # A list with no even numbers

# Test with numbers1
print(f"Checking list: {numbers1}")
found_even = False # Flag to track if an even number was found
for num in numbers1:
    if num % 2 == 0:
        print(f"Found the first even number: {num}")
        found_even = True
        break
# The 'else' block below executes ONLY if the loop completes without a 'break'
else:
    if not found_even: # This check is technically redundant if 'else' is used correctly, but makes it clearer for beginners.
        print("No even numbers found in this list.")

# Test with numbers2
print(f"\nChecking list: {numbers2}")
for num in numbers2:
    if num % 2 == 0:
        print(f"Found the first even number: {num}")
        break
else: # This 'else' belongs to the 'for' loop and executes if 'break' is not hit
    print("No even numbers found in this list.")

print("Finding First Even Number finished.\n")

# --- Problem: Printing Odd Numbers Only ---
print("\n--- Printing Odd Numbers Only ---")

print(f"Printing odd numbers from 1 to 10...")
for i in range(1, 11):
    if i % 2 == 0:
        continue
    else:
        print(i)

print(f"Printing Odd Numbers Only finished.\n")