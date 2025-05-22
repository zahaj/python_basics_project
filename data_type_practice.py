# Basic Arithmetic for Numbers
# num1 = 38
# num2 = 17

num1 = int(input("Specify the first integer number: "))
num2 = int(input("Specify the second integer number: "))
sum_nums = num1 + num2
subtracted_nums = num1 - num2
multip_nums = num1 * num2
divis_nums = num1 / num2
integer_divis_nums = num1 // num2
modulo_nums = num1 % num2
exponent_nums = num1 ** num2
print(f"""For num1 = {num1} and num2 = {num2} their:
sum is {sum_nums},
difference: {subtracted_nums},
product: {multip_nums},
quotient: {divis_nums},
integer division: {integer_divis_nums},
modulo: {modulo_nums}.
num1 to the power of num2 equals to {exponent_nums}.
The type of division is {type(divis_nums)} and the type of integer division is
{type(integer_divis_nums)}.
""")

# Type Conversion Examples
price_str = "150.75"
actual_price = float(price_str)
quantity = 3
total_cost = actual_price * quantity
print(f"The price as a string is {price_str}. The price converted to float is {actual_price}.")
print(f"The total cost is {total_cost}. The type of this variable is {type(total_cost)}.")
print(f"The total cost after converting to integer is {int(total_cost)}.")

print(f"The sum of 0.1 and 0.2 is {0.1 + 0.2}.")

# Strings and Text Manipulation
# first_name = "Ada"
# last_name = "Lovelas"
first_name = input("What is your first name? ")
last_name = input("What is your last name? ")

full_name = first_name + " " + last_name
print(f"Hello, {full_name}! Welcome to the Python world.")
age = input("What is your age? ")
# age = 20
print(f"{full_name} is {age} years old.")

message = " Python programming is FUN! "
print(f"{message.upper()}, {message.lower()}, {message.strip()}, {message.replace('FUN', 'AWSOME')}.")
message_to_list = message.strip().upper().split(" ")
print(message_to_list)

sentence = "The quick brown fox jumps over the lazy dog."
print(f"""The sentence is "{sentence}".
The first word is "{sentence[:3]}", the last word is "{sentence[-4:-1]}".
The entire sentence in reverse is: "{sentence[::-1]}.
This is a phrase from the sentence: "{sentence[10:19]}".
""")

# Booleans and Logical Operations
# x = 10
# y = 20
x = float(input("Specify the first number: "))
y = float(input("Specify the second number: "))

print(f"""x is equal to {x}, y is equal to {y}.
Let's check the following Comparison Operators:
x == y: {x == y},
x != y: {x != y},
x > y: {x > y},
x >= y: {x >= y},
x < y: {x < y},
x <= y: {x <= y}
""")

"""
print(
    f"x is equal to {x}, y is equal to {y}.\n"
    f"The following is true:\n"
    f" x == y: {x == y},\n"
    f" x != y: {x != y},\n"  # Fixed potential typo here
    f" x > y: {x > y},\n"
    f" x >= y: {x >= y},\n"
    f" x < y: {x < y},\n"
    f" x <= y: {x <= y}.\n"
)
"""
is_sunny = True
is_weekend = False
print(f"""is_sunny equals to True, is_weekend equals to False.
Let's check the following Logical Operators (and, or, not):
is_sunny and is_weekend: {is_sunny and is_weekend},
is_sunny or is_weekend: {is_sunny or is_weekend},
not is_sunny: {not is_sunny},
(is_sunny and not is_weekend) or (not is_sunny and is_weekend) : {(is_sunny and not is_weekend)
or (not is_sunny and is_weekend)}.
""")
# Challenge: is a user eligible to vote?
age = 19
is_registered = True
print(f"""Your age is {age} and you are registered {is_registered}.
Can you vote? {age >= 18 and is_registered == True}.""")