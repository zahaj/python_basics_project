# Using if - else statement

# Check if the input number is positive
number = int(input("Give me the integer number: "))
if number > 0:
    print("The number is positive.")
else:
    print("The number is not positive (it's negative or zero).")

# check if the input number is even or odd
number2 = int(input("Give me another integer number: "))
if number2 % 2 == 0:
    print("The number is even.")
else:   
    print("The number is odd.")

# print a letter grade for an input of numeric score
grade = int(input("Enter your score (0-100): "))
if 90 <= grade <= 100:
    print("Your letter grade is 'A'")
elif 80 <= grade <= 89:
    print("Your letter grade is 'B'")
elif 70 <= grade <= 79:
    print("Your letter grade is 'C'")
elif 60 <= grade <= 69:
    print("Your letter grade is 'D'")
elif grade < 60:
    print("Your letter grade is 'F'")
"""
score_str = input("Enter score (0-100): ")
try:
    score = int(score_str)
    if not (0 <= score <= 100): # Check for valid range first
        print("Invalid score. Please enter a number between 0 and 100.")
    elif score >= 90:
        print("Grade: A")
    elif score >= 80:
        print("Grade: B")
    elif score >= 70:
        print("Grade: C")
    elif score >= 60:
        print("Grade: D")
    else: # This implicitly means score < 60 due to previous checks
        print("Grade: F")
except ValueError:
    print("Invalid input. Please enter a valid number.")
"""
# print greetings depending on a current hour specified by a user
current_hour = int(input("Specify the current hour in 24-hour format: "))
if 12 > current_hour >= 5:
    print("Good morning!")
elif 18> current_hour >= 12:
    print("Good afternoon!")
elif current_hour >= 18 or current_hour < 5:
    print("Good evening!")

# check if a user with specified age and the registration status is eligible to vote
user_age = int(input("Enter your age: "))
registered_to_vote = input("Are you registered to vote (yes/no)? ")
if registered_to_vote.lower() == "yes":
    is_registered = True
elif registered_to_vote.lower() == "no":
    is_registered = False

if user_age >= 18:
    if is_registered == True:
        print("You are eligible to vote and registered!")
    else:
        print("You are old enough to vote but not registered.")
else:
    print("You are not old enough to vote.")

# check if username and password entered by a user matches data for admin 
correct_username = "admin"
correct_password = "password123"
username_input = input("Enter your user name: ")
password_input = input("Enter your password: ")

if username_input == correct_username and password_input == correct_password:
    print("Login successful!")
# Usually you don't want to reveal which one is wrong for security,
# it's only for practicing conditionals purposes.
elif username_input != correct_username and password_input == correct_password:
    print("Invalid username.")
elif username_input == correct_username and password_input != correct_password:
    print("Invalid password.")
# else:
#    print("Invalid username or password.")