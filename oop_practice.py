# Day 4: Object-Oriented Programming (OOP) - Structuring Complex Programs!

from typing import List, Union, Any, Optional

### Practical Problems: Basic Classes & Objects

# 1. Simple Dog Class
print("\n--- Problem 1: Simple Dog Class ---")

class Dog:
    """A very basic Dog class without a constructor."""
    name = "Buddy"
    breed = "Golden Retriever"

    def bark(self): # 'self' refers to the instance of the class (the specific dog object)
        """Prints barking sound 'Woof!'."""
        print("Woof!")

# Create an instance of the Dog class
dog = Dog()

# Access and print attributes
print(f"Dog's name: {dog.name}")
print(f"Dog's breed: {dog.breed}")

# Call the Dog class method
dog.bark()

# 2. Introducing __init__ (Constructor) and self
print("\n--- Problem 2: Introducing __init__ (Constructor) and self ---")


# Redefining Dog class to add __init__
class Dog:
    """A Dog class with an __init__ method for initialization."""

    def __init__(self, name: str, breed: str):
        """
        Initializes a new Dog instance.

        Args:
            name (str): The name of the dog.
            breed (str): The breed of the dog.
        """
        self.name = name # Instance attribute
        self.breed = breed # Instance attribute
        print(f"A new dog named {self.name} ({self.breed}) has been created!")

    def bark(self):
        """Makes the dog bark, including its name."""
        print(f"{self.name} says Woof!")

#Create two new Dog objects
dog1 = Dog("Max", "German Shepherd")
dog2 = Dog("Lucy", "Beagle")

# Access and print attributes
print(f"Dog 1: {dog1.name}, {dog1.breed}")
print(f"Dog 2: {dog2.name}, {dog2.breed}")

# Call methods on two Dog objects
dog1.bark()
dog2.bark()

# 3. Class Attributes vs. Instance Attributes
print("\n--- Problem 3: Class vs. Instance Attributes ---")

class Dog:

    """A Dog class with an __init__ method for initialization and ."""

    # Class attributes (shared by all instances of this class)
    number_of_legs = 4
    dog_count = 0

    def __init__(self, name: str, breed: str):
        """
        Initializes a new Dog instance and increments the dog_count.

        Args:
            name (str): The name of the dog.
            breed (str): The breed of the dog.
        """
        self.name = name # Instance attribute
        self.breed = breed # Instance attribute
        # Increment class attribute every time a new Dog is created
        Dog.dog_count += 1
        print(f"A new dog named {self.name} ({self.breed}) has been created!")

    def bark(self):
        """Makes the dog bark, including its name."""
        print(f"{self.name} says Woof!")

# Create two Dog instances
dog1 = Dog("Max", "German Shepherd")
dog2 = Dog("Lucy", "Beagle")

# Access class attribute directly via the class
print(f"All dogs have {Dog.number_of_legs} legs.")

# Access class attribute via instance (also works, but looks up to class)
print(f"{dog1.name} has {dog1.number_of_legs} legs.") 
print(f"{dog2.name} has {dog2.number_of_legs} legs.") 

# Print dog_count after creating two dogs
print(f"Number of Dog instances created: {Dog.dog_count}.")

# Create a third dog
dog3 = Dog("Bella", "Poodle")
print(f"Number of Dog instances created: {Dog.dog_count}.")

# 4. Car Class Example
print("\n--- Problem 4: Car Class Example ---")

class Car:
    """A Car class """
    
    wheels = 4 # Class attribute: all cars typically have 4 wheels

    def __init__(self, make: str, model: str, year: int):
        """Initializes a new Car instance.
        
        Args:
            make (str): The make of the car (e.g., 'Toyota').
            model (str): The model of the car (e.g., 'Camry').
            year (int): The manufacturing year.
        """
        self.make = make
        self.model = model
        self.year = year
    
    def display_car_info(self):
        """Prints the car's details."""
        print(f"The car: {self.make}, {self.model}, {self.year} and number of wheels {self.wheels}.") # self.wheels or Car.wheels

# Creating two Car instances
car1 = Car("Toyota", "Camry", 1989)
car2 = Car("Audi", "A4", 2000)

# Displaying info about two cars with method display_car_info
car1.display_car_info()
car2.display_car_info()

# Try changing Car.wheels for all cars by modifying the class attribute
print("\nChanging Car.wheels to 3 ")
# Changing class atribute and checking 
Car.wheels = 3 # This changes the class attribute
car1.display_car_info() # Both cars now show 3 wheels
car2.display_car_info()
print("Changing a class attribute affects all instances unless they have their own instance attribute with the same name.")

### Practical Problems: Inheritance & Polymorphism

# 1. Basic Inheritance (Vehicle -> Car, Motorcycle):
print("\n--- Problem 1: Basic Inheritance (Vehicle -> Car, Motorcycle) ---")

# Parent Class: Define a Vehicle class.
class Vehicle:
    """Base class for all vehicles."""

    def __init__(self, make: str, model: str):
        """Initializes a Vehicle instance.

        Args:
            make (str): The make of the car (e.g., 'Toyota').
            model (str): The model of the car (e.g., 'Camry').
        """
        self.make = make
        self.model = model

    def start_engine(self):
        """Starts the vehicle's engine."""
        print(f"The {self.make} {self.model} engine starts.")

# Child Class 1: Define a Car class that inherits from Vehicle.
class Car(Vehicle):
    """A Car is a type of Vehicle with a specific number of doors."""

    def __init__(self, make: str, model: str, num_doors: int):
        """
        Initializes a Car instance.

        Args:
            make (str): The make of the car.
            model (str): The model of the car.
            num_doors (int): The number of doors on the car.
        """
        super().__init__(make, model) # Call Vehicle's __init__
        self.num_doors = num_doors # Car-specific attribute
        
    def drive(self):
        """Simulates the car driving."""
        print(f"The {self.make} {self.model} is driving on 4 wheels.")
        # Using hasattr to reference a potential 'wheels' class attribute if it exists, otherwise default.
        print(f"The {self.make} {self.model} is driving on {self.wheels if hasattr(self, 'wheels') else 4} wheels.")


# Child Class 2: Define a Motorcycle class that inherits from Vehicle.
class Motorcycle(Vehicle): # Motorcycle inherits from Vehicle
    """A Motorcycle is a type of Vehicle, with an option for a sidecar."""

    def __init__(self, make: str, model: str, has_sidecar: bool): # !!! booleann niby nie O.K. 
        """Initializes a Motorcycle instance.
        
        Args:
            make (str): The make of the motorcycle.
            model (str): The model of the motorcycle.
            has_sidecar (bool): True if the motorcycle has a sidecar, False otherwise.
        """
        super().__init__(make, model) # Call the parent class's __init__ method
        self.has_sidecar = has_sidecar     
    
    def ride(self):
        """Simulates the motorcycle riding."""

        sidecar_info = "with a sidecar" if self.has_sidecar else "without a sidecar"

        print(f"The {self.make} {self.model} is riding on 2 wheels {sidecar_info}.")

# Create an instance of a Car and a Motorcycle
generic_vehicle = Vehicle("Generic", "Vehicle Model X")
car = Car("Honda", "Civic", 2)
motorcycle = Motorcycle("BMV", "F1200", False)

# Call start_engine (inherited method)
generic_vehicle.start_engine()
car.start_engine()
motorcycle.start_engine()

# Call specific methods:
car.drive()
motorcycle.ride()

# 2. Polymorphism
print("\n--- Problem 2: Polymorphism ---")

# Create a list called garage that contains a mix of Vehicle, Car, and Motorcycle objects.
garage: list[Vehicle] = [
    Vehicle("Generic", "Commuter"),
    Car("Toyota", "Camry", 4),
    Motorcycle("Harley", "Fat Boy", False)
]

# Call the same method on different objects
print("Looping through the garage and starting engines (polymorphism in action):")
for item in garage:
    # The same method call 'start_engine()' behaves differently
    # depending on the actual type of the 'item' object.
    # start_engine() method uses instance-specific attributes (self.make and self.model).
    item.start_engine()


# 2. Polymorphism
print("\n--- Problem 2: Polymorphism ---")
# Create a list containing a mix of Vehicle, Car, and Motorcycle objects
garage: List[Vehicle] = [
    Vehicle("Generic", "Commuter"),
    Car("Honda", "CR-V", 5),
    Motorcycle("Ducati", "Monster", False),
    Car("Tesla", "Model 3", 4),
    Vehicle("Scooter", "Electric")
]

print("Looping through the garage and starting engines (polymorphism in action):")
for item in garage:
    # The same method call 'start_engine()' behaves differently
    # depending on the actual type of the 'item' object.
    item.start_engine()


### Practical Problems: Encapsulation Basics & Special Methods ###
print("\n--- Problem 3: Encapsulation Basics & __str__ ---")


# 1. Encapsulation Basics (_private_like attributes):

# Revisiting the Dog class
print("\n1: Encapsulation Basics (_private_like attributes)")
class Dog: # Redefining Dog class to include _age and __str__
    """
    A Dog class demonstrating encapsulation conventions and __str__ method.
    We use a single underscore prefix (_age) to indicate a "protected" or
    "private-like" attribute, meaning it's intended for internal use only.
    """

    def __init__(self, name: str, breed: str, age: Union[int, float]):
        """
        Initializes a new Dog instance.

        Args:
            name (str): The name of the dog.
            breed (str): The breed of the dog.
            age (Union[int, float]): The age of the dog.
        """
        self.name = name # Instance attribute
        self.breed = breed # Instance attribute
        self._age = age # Convention: single underscore for 'protected' attribute

        print(f"A new dog named {self.name} ({self.breed}) has been created!")

    def get_age(self):
        """Returns the dog's age."""
        return self._age
    
    def set_age(self, new_age: Union[int, float]):
        """
        Sets the dog's age after validation.

        Args:
            new_age (Union[int, float]): The new age to set.
        """
        if isinstance(new_age, (int, float)) and new_age > 0:
            self._age = new_age
            print(f"{self.name}'s age updated to {new_age}.")
        else:
            print(f"Error: Invalid age '{new_age}'. Age must be a non-negative integer or float.")

# Create a Dog object, set its age.
my_dog = Dog("Max", "Puddle", 10.5)

# Test Dog's class method with different input
print(f"Setting new age for the dog: 13.5.")
my_dog.set_age(13.5)
print(f"The dog is {my_dog.get_age()} years old.")
print(f"Setting invalid (str) age for the dog: 'Thirteen'.")
my_dog.set_age('Thirteen')
print(f"The dog is {my_dog.get_age()} years old.")
print(f"Setting new age for the dog: -5.")
my_dog.set_age(-5)
print(f"The dog is {my_dog.get_age()} years old.")

# 2. __str__ (String Representation for Users):

# Revisiting the Dog class
print("\n--- __str__ (String Representation for Users) ---")
class Dog: # Redefining Dog class to include _age and __str__
    """
    A Dog class demonstrating encapsulation conventions and __str__ method.
    We use a single underscore prefix (_age) to indicate a "protected" or
    "private-like" attribute, meaning it's intended for internal use only.
    """

    def __init__(self, name: str, breed: str, age: Union[int, float]):
        """
        Initializes a new Dog instance.

        Args:
            name (str): The name of the dog.
            breed (str): The breed of the dog.
            age (Union[int, float]): The age of the dog.
        """
        self.name = name # Instance attribute
        self.breed = breed # Instance attribute
        self._age = age # Convention: single underscore for 'protected' attribute

        print(f"A new dog named {self.name} ({self.breed}) has been created!")

    def __str__(self):
        """Defines a string represantation of the Dog class object.
        It gives information about the object that is easy for a human to understand. and interpret quickly.
        When you print(my_object), Python implicitly calls str(my_object), which in turn calls my_object.__str__().
        It must return a string (str).
        """
        return f"Dog(Name: {self.name}, Breed: {self.breed}, Age: {self._age})" # This is for the user!
    
    def get_age(self):
        """Returns the dog's age."""
        return self._age
    
    def set_age(self, new_age: Union[int, float]):
        """
        Sets the dog's age after validation.

        Args:
            new_age (Union[int, float]): The new age to set.
        """
        if isinstance(new_age, (int, float)) and new_age > 0:
            self._age = new_age
            print(f"{self.name}'s age updated to {new_age}.")
        else:
            print(f"Error: Invalid age '{new_age}'. Age must be a non-negative integer or float.")

doggy = Dog("George", "Terrier", 6.5)
print(f"Using: print(doggy): {doggy}.")
print(f"Using: print(str(doggy)): {str(doggy)}.")
print(f"Using: print(doggy.__str__())): {doggy.__str__()}.")

### Practical Problems: Simple Project - Putting it all together (BankAccount) ###

# 1. BankAccount Class
#### Practical Problems: Simple Project - Putting it all together (`BankAccount`) ####
print("\n--- Problem 4: Simple Project - BankAccount ---")

class BankAccount:
    """
    Represents a simple bank account with deposit, withdrawal, and balance tracking.
    """
    def __init__(self, account_holder: str, initial_balance: float = 0.0):
        """
        Initializes a new BankAccount.

        Args:
            account_holder (str): The name of the account holder.
            initial_balance (float): The initial balance of the account. Defaults to 0.0.

        Raises:
            ValueError: If initial_balance is negative.
        """
        if not isinstance(account_holder, str) or not account_holder.strip():
            raise ValueError("Account holder name cannot be empty.")
        if not isinstance(initial_balance, (int, float)) or initial_balance < 0:
            raise ValueError("Initial balance must be a non-negative number.")

        self.account_holder = account_holder
        self._balance = float(initial_balance) # Using _ for internal balance management

    def deposit(self, amount: float) -> None:
        """
        Deposits a specified amount into the account.

        Args:
            amount (float): The amount to deposit. Must be positive.
        """
        if not isinstance(amount, (float, int)) or amount <= 0:
            print(f"Deposit Error: Invalid amount '{amount}'. Amount must be a positive number.")
            return
        self._balance += amount
        print(f"Deposited ${amount:.2f}. New balance: ${self._balance:.2f}")


    def withdraw(self, amount: float):
        """
        Withdraws a specified amount from the account.

        Args:
            amount (float): The amount to withdraw. Must be positive.
        """
        if not isinstance(amount, (float, int)) or amount <= 0:
            print(f"Withdrawal Error: Invalid amount '{amount}'. Amount must be a positive number.")
            return
        if amount > self._balance:
            print(f"Withdrawal Error: Insufficient funds. Current balance: ${self._balance:.2f}, Attempted withdrawal: ${amount:.2f}.")
        else:
            self._balance -= amount
            print(f"Withdrew ${amount:.2f}. New balance: ${self._balance:.2f}")

    def get_balance(self) -> float:
        """
        Returns the current balance of the account.
        """
        return self._balance

    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the BankAccount.
        """
        return f"Account for {self.account_holder}: Balance = ${self._balance:.2f}"

# --- BankAccount Demonstration ---
print("\n--- BankAccount Demonstration ---")

try:
    # Create an instance of BankAccount class
    my_bank_account = BankAccount("Eva", 100)
    # Print the account object directly to see the __str__ in action   
    print(my_bank_account)
    my_bank_account.deposit(99.50)
    # Test valid deposit and withdraw
    print(f"Current balance for {my_bank_account.account_holder}: {my_bank_account.get_balance()}")
    my_bank_account.withdraw(50.25)
    print(f"Current balance for {my_bank_account.account_holder}: {my_bank_account.get_balance()}")
    my_bank_account.deposit(150)
    print(f"Current balance for {my_bank_account.account_holder}: {my_bank_account.get_balance()}")
    # Test insufficient funds withdrawal
    my_bank_account.withdraw(1500.00)
    print(f"Current balance for {my_bank_account.account_holder}: {my_bank_account.get_balance()}")
    # Test invalid deposit/withdrawal amounts.
    my_bank_account.deposit(-50.00)
    print(f"Current balance for {my_bank_account.account_holder}: {my_bank_account.get_balance()}")

    # Test edge case for initial balance
    try:
        invalid_account = BankAccount("Jane Smith", -50.00)
    except ValueError as e:
        print(f"Caught expected error creating account with negative balance: {e}")

    try:
        invalid_account_name = BankAccount("", 100.00)
    except ValueError as e:
        print(f"Caught expected error creating account with empty name: {e}")

except ValueError as e:
    print(f"Initialization Error: {e}")