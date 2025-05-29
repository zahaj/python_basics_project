# Day 5: Advanced OOP & Testing Basics

from typing import List, Union, Any, Optional
from abc import ABC, abstractmethod
import math
import datetime

class InsufficientFundsError(Exception):
    """Raised when a bank account withdrawal is attempted with insufficient funds."""
    pass

class InvalidAmountError(Exception):
    """Raised when a deposit or withdrawal amount is zero, negative, or non-numeric."""
    pass

# Simple Data Logging
def log_transaction(account_holder: str, transaction_type: str, amount: float, current_balance: float):
    """Logs a bank transaction to 'bank_transactions.log'."""

    if not isinstance(account_holder, str) or not account_holder.strip():
        raise ValueError("Account holder must be a non-empty string")
    if not isinstance(transaction_type, str) or not transaction_type.strip():
        raise ValueError("Account holder must be a non-empty string")
    if not isinstance(amount, (float, int)) or amount <= 0:
        raise ValueError("Amount must be a positive number")
    if not isinstance(current_balance, (float)):
        raise ValueError("Current balance must be a number")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = (
        f"{timestamp} | Account: {account_holder} | Type: {transaction_type} | "
        f"Amount: {amount:.2f} | Balance: {current_balance:.2f}\n"
    )
    # Appending transaction log to a log file 
    log_file_name = 'bank_transactions.log'
    
    try:
        with open(log_file_name, "a") as log_file:
            log_file.write(log_message)
        print(f"Logged transaction for {account_holder}: {transaction_type} ${amount:.2f}")
    except OSError as e:
        print(f"ERROR: Could not write to log file: {e}")

class BankAccount:
    """
    Represents a simple bank account with deposit, withdrawal, and balance tracking.
    """
    def __init__(self, account_holder: str, initial_balance: float = 0.0):
        if not isinstance(account_holder, str) or not account_holder.strip():
            raise ValueError("Account holder name cannot be empty.")
        if not isinstance(initial_balance, (int, float)) or initial_balance < 0:
            raise ValueError("Initial balance must be a non-negative number.")

        self.account_holder = account_holder
        self._balance = float(initial_balance) # Internal balance storage

    @property
    def balance(self) -> float:
        """The current balance of the account."""
        return self._balance

    """Do not create a balance.setter. This ensures that balance can only be changed
    internally by deposit() and withdraw(), not by direct assignment from outside
    (my_account.balance = 500 would cause an error, which is good!)."""

    def deposit(self, amount: float) -> None:
        if not isinstance(amount, (float, int)) or amount <= 0:
            raise InvalidAmountError("Deposit amount must be a positive number.")
            # return  # Not necessary anymore - raise already stops execution
        
        self._balance += amount
        print(f"Deposited ${amount:.2f}. New balance: ${self._balance:.2f}")
        log_transaction(self.account_holder, "Deposit", amount, self._balance)

    def withdraw(self, amount: float):
        if not isinstance(amount, (float, int)) or amount <= 0:
            raise InvalidAmountError("Withdraw amount must be a positive number.")
            # return # Not necessary anymore - raise already stops execution
        if amount > self._balance:
            raise InsufficientFundsError("Cannot withdraw: Not enough money in the account.")
        else:
            self._balance -= amount
            print(f"Withdrew ${amount:.2f}. New balance: ${self._balance:.2f}")
            log_transaction(self.account_holder, "Withdraw", amount, self._balance)

    def __str__(self) -> str:
        return f"Account for {self.account_holder}: Balance = ${self._balance:.2f}"

# --- BankAccount Demonstration ---
print("\n--- BankAccount Demonstration ---")

# Create an instance of BankAccount class
my_bank_account = BankAccount("Eva", 100)
print(my_bank_account)
print(f"Accessing balance via property: ${my_bank_account.balance:.2f}")

# Test deposit with custom exceptions
try:
    my_bank_account.deposit(100)
    my_bank_account.deposit(0) # Should raise InvalidAmountError
except InvalidAmountError as e:
    print(f"Caught Error (deposit): {e}")
except Exception as e:
    print(f"Caught unexpected error: {e}")

try: 
    my_bank_account.deposit("20") # Should raise InvalidAmountError
except InvalidAmountError as e:
    print(f"Caught Error (deposit): {e}")
except Exception as e:
    print(f"Caught unexpected error: {e}.")

try:
    my_bank_account.withdraw(-20) # Should raise InvalidAmountError
except InvalidAmountError as e:
    print(f"Caught Error (withdrawal negative amount): {e}")

try:
    my_bank_account.withdraw(20)
    my_bank_account.withdraw(1500) # Should raise InsufficientFundsError
except InsufficientFundsError as e:
    print(f"Caught Error (withdrawal): {e}")
except InvalidAmountError as e:
     print(f"Caught Error (withdrawal amount): {e}")   
except Exception as e:
    print(f"Caught unexpected error: {e}")

print(f"Final Balance for {my_bank_account.account_holder}: ${my_bank_account.balance:.2f}")

# Try to set balance directly (should raise AttributeError)
print("Attempt to directly assign the balance...")
try:
    my_bank_account.balance = 1000
except AttributeError as e:
    print(f"Caught Expected Error: {e}")
except Exception as e:
    print(f"Caught unexpected Error: {e}")

# Practical Problem 2.1: Dog Class with Properties

class Dog: # Redefining Dog class to include properties
    def __init__(self, name: str, breed: str, age: int):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Dog's name must be a non-empty string.")
        if not isinstance(breed, str) or not breed.strip():
            raise ValueError("Dog's breed must be a non-empty string.")
        if not isinstance(age, int) or age < 0:
            raise ValueError(f"Age must be a non-negative integer.")
        self.name = name
        self.breed = breed
        # Call the setter for initial validation
        self.age = age # (instead od self._age = age) it will automatically use new age.setter below for initial validation
        print(f"A new dog named {self.name} ({self.breed}) has been created!")

    @property # This decorates the getter method
    def age(self):
        # print("DEBUG: Getting age...")
        return self._age # Returns the internal value
    
    @age.setter  # Decorator for the setter method
    def age(self, new_age: int): # setter property with validation
        # print(f"DEBUG: Setting age to {new_age}...")
        if not isinstance(new_age, int) or new_age < 0:
            raise ValueError(f"Invalid age '{new_age}'. Age must be a non-negative integer.")
        
        self._age = new_age # Sets the internal value
        # my_object.my_value = 50 calls this setter method, allowing the validation

    def bark(self):
        print(f"{self.name} says Woof!")

    def __str__(self) -> str:
        return f"Dog(Name: {self.name}, Breed: {self.breed}, Age: {self.age})" # self.age will now use the age.getter

    def __repr__(self):
        return f"Dog(name='{self.name}', breed='{self.breed}', age={self.age})"    

# --- Dog Demonstration ---
print("\n--- Dog Demonstration ---")

my_dog = Dog("George", "Terrier", 6)
print(my_dog)

print(f"Dog's age (via property): {my_dog.age}.") # show the getter working
print(f"Setting dog's age to 8...")
my_dog.age = 8 # Using setter
print(my_dog.__repr__())

print("Attempting to set dog's age to a float (10.5)...")
try:
    my_dog.age = 10.5 # Should raise ValueError
except ValueError as e:
    print(f"Caught Error: {e}")
    print(f"Dog's age after invalid attempt: {my_dog.age}") # Age should be unchanged
except Exception as e:
    print(f"An unexpected error occured : {e}")
    print(f"Dog's age after invalid attempt: {my_dog.age}") # Age should be unchanged

print("Attempting to set dog's age to a negative number (-2)...")
try:
    my_dog.age = -2 # Should raise ValueError
except ValueError as e:
    print(f"Caught error : {e}")
    print(f"Dog's age after invalid attempt: {my_dog.age}") # Age should be unchanged
except Exception as e:
    print(f"An unexpected error occured : {e}")
    print(f"Dog's age after invalid attempt: {my_dog.age}") # Age should be unchanged

class Vehicle:
    def __init__(self, make: str, model: str):
        if not isinstance(make, str) or not make:
            raise ValueError("Make must be a non-empty string.")
        if not isinstance(model, str) or not model:
            raise ValueError("Model must be a non-empty string.")
        self.make = make
        self.model = model

    def start_engine(self):
        print(f"The {self.make} {self.model} engine starts.")

class Engine:
    def __init__(self, horsepower: int):
        if not isinstance(horsepower, int) or horsepower <= 0:
            raise ValueError("Engine horsepower must be a positive integer.")
        self.horsepower = horsepower

    def start(self):
        print(f"Engine with {self.horsepower} horsepower started.")
    
    def stop(self):
        print(f"Engine {self.horsepower} stopped.")

class Wheel:
    def __init__(self, size: int):
        if not isinstance(size, int):
            raise ValueError("Wheel size must be a positive integer.")
        self.size = size

    def roll(self):
        print(f"Wheel of size {self.size} rolling.")

class Radio:
    def __init__(self, brand: str):
        if not isinstance(brand, str) or not brand.strip():
            raise ValueError("Radio brand must be a non-empty string.")
        self.brand = brand
        self._is_on = False
    
    def play_music(self):
        if not self._is_on:
            self._is_on = True
            print(f"Turning on {self.brand} radio and playing music.")
        else:
            print(f"{self.brand} radio already on, playing music.")
    
    def change_station(self):
        if self._is_on:
            print("Radio changing station.")
        else:
            print(f"Cannot change station, {self.brand} radio is off.")

    def turn_off(self):
        if self._is_on:
            print(f"Turning off {self.brand} radio.")
            self._is_on = False
        else:
            print(f"Radio {self.brand} is already off.")

    def __str__(self):
        return f"Radio({self.brand})"
    def __repr__(self):
        return f"Radio(brand='{self.brand}')"


class Car(Vehicle): # Car IS-A Vehicle
    def __init__(self, make: str, model: str, num_doors: int, engine: Engine, radio: Radio):
        super().__init__(make, model) # Call Vehicle's __init__
        if not isinstance(num_doors, int) or num_doors <= 0:
            raise ValueError("Number of doors must be a positive integer.")
        if not isinstance(engine, Engine):
            raise TypeError("Engine must be an instance of Engine class.")
        if not isinstance(radio, Radio):
            raise TypeError("Radio must be an instance of Radio class.")
        self.num_doors = num_doors # Car-specific attribute
        self.engine = engine # Car HAS-A Engine
        self.radio = radio   # Car HAS-A Radio
        self.wheels: List[Wheel] = [Wheel(18) for _ in range(4)] # Car HAS-A list of Wheels
        
    def drive(self):
        print(f"The {self.make} {self.model} is driving on 4 wheels.")
        # Using hasattr to reference a potential 'wheels' class attribute if it exists, otherwise default.
        print(f"The {self.make} {self.model} is driving on {self.wheels if hasattr(self, 'wheels') else 4} wheels.")

    def start_driving(self):
        print(f"\n--- Starting {self.make} {self.model} ---")
        self.engine.start()
        for wheel in self.wheels:
            wheel.roll()
        print(f"The {self.make} {self.model} is now driving.")

    def stop_driving(self):
        print(f"\n--- Stopping {self.make} {self.model} ---")
        self.engine.stop()
        self.radio.turn_off()
        print(f"The {self.make} {self.model} has stopped.")

    def play_car_radio(self):
        self.radio.play_music()

    def __str__(self):
        return (f"Car(Make: {self.make}, Model: {self.model}, Doors: {self.num_doors}, "
                f"Engine: {self.engine}, Radio: {self.radio}, Wheels: {[str(w) for w in self.wheels]})")

    def __repr__(self):
        return (f"Car(make='{self.make}', model='{self.model}', num_doors={self.num_doors}, "
                f"engine={repr(self.engine)}, radio={repr(self.radio)})")

# --- Car with Composition Demonstration ---
print("\n--- Car class with Composition Demonstration ---")

# Create component objects
bose_radio = Radio(brand="Bose")
v8_engine = Engine(horsepower=400)

# Create a Car instance using these component objects
car = Car(make="Porsche", model="Cayenne", num_doors=2, engine=v8_engine, radio=bose_radio)

print(car)
print(f"Car's engine: {car.engine.horsepower} HP")
print(f"Car's radio brand: {car.radio.brand}.")
print(f"Car has {len(car.wheels)} wheels.")

car.start_driving()
car.play_car_radio()
car.radio.change_station() # Direct interaction with composed object
car.engine.stop()
car.stop_driving()

class Shape:
    """This is a base class for different shapes."""

    def area(self) -> int:
        """Calculates the area of the shape."""
        return 0

    def perimeter(self):
        """Calculates the perimeter of the shape."""
        return 0
    
    def __str__(self):
        return f"Shape()"
    
    def __repr__(self):
        return f"Shape()"
    
class Circle(Shape):

    def __init__(self, radius: Union[int, float]):
        if not isinstance(radius, (int, float)) or radius <= 0:
            raise ValueError("Radius must be a positive number")
        self.radius = radius

    def area(self):
        """Calculates an area of a circle."""
        area = math.pi * self.radius ** 2
        return area
    
    def perimeter(self):
        """Returns a perimeter of a circle."""
        perimeter = 2 * math.pi * self.radius
        return perimeter

    def __str__(self):
        return f"Circle(Radius: {self.radius})"

    def __repr__(self):
        return f"Circle(radius={self.radius})"

class Rectangle(Shape):
    
    def __init__(self, length: Union[int, float], width: Union[int, float]):
        if not isinstance(length, (int, float)) or length <= 0:
            raise ValueError("Length must be a positive number")
        if not isinstance(width, (int, float)) or width <= 0:
            raise ValueError("Width must be a positive number")
        self.length = length
        self.width = width
    
    def area(self):
        """Returns an area of a rectangle with sides: length and width."""
        area =  self.length * self.width
        return area

    def perimeter(self):
        """Returns a perimeter of a rectangle with sides: length and width."""
        perimeter = 2 * (self.length + self.width)
        return perimeter
    
    def __str__(self):
        return f"Rectangle(Length: {self.length}, Width: {self.width})"

    def __repr__(self):
        return f"Rectangle(length={self.length}, width={self.width})"

class Vector:

    def __init__(self, x: Union[int, float], y: Union[int, float]):
        # First, explicitly check if the type is boolean and disallow it
        if isinstance(x, bool): # Check for bool first!
            raise TypeError("Vector x-coordinate cannot be a boolean value.")
        if not isinstance(x, (int, float)):
            raise TypeError("Vector x-coordinate must be a number.")
        # First, explicitly check if the type is boolean and disallow it
        if isinstance(y, bool): # Check for bool first!
            raise TypeError("Vector y-coordinate cannot be a boolean value.")
        if not isinstance(y, (int, float)):
            raise TypeError("Vector y-coordinate must be a number.")
        self.x = x
        self.y = y

    def __add__(self, other):
        """Implements vector addition (self + other)."""
        if not isinstance(other, Vector):
            raise TypeError(f"Unsupported operand type for +: 'Vector' and '{type(other).__name__}'")
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Implements vector subtraction (self - other)."""
        if not isinstance(other, Vector):
            raise TypeError(f"Unsupported operand type for -: 'Vector' and '{type(other).__name__}'")
        return Vector(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        """Implements vector equality (self == other)"""
        if not isinstance(other, Vector):
            return NotImplemented #or False, depending on strictness
        return (self.x == other.x) and (self.y == other.y)

    def __ne__(self, other):
        """Implements vector inequality (self != other)"""
        if not isinstance(other, Vector):
            return NotImplemented # Or False, depending on strictness
            """Crucial Point: When a comparison method (like __eq__, __ne__, __lt__, etc.) returns NotImplemented,
            Python doesn't immediately raise an error. Instead, it tries a reverse operation if one is available.
            For a != b, if a.__ne__(b) returns NotImplemented, Python then tries b.__ne__(a).
            If b (e.g., a string or None) doesn't have a meaningful __ne__ that handles Vector objects, or if it
            also returns NotImplemented, then Python falls back to a default behavior for !=.
            The default behavior for a != b when neither object can explicitly compare is generally to return
            the opposite of a is b (identity comparison)."""
        return (self.x != other.x) or (self.y != other.y)

    def __mul__(self, scalar: Union[int, float]):
        """Implements scalar multiplication (vector * scalar)."""
        if not isinstance(scalar, (int, float)):
            raise TypeError(f"Unsupported operand type for *: 'Vector' and '{type(scalar).__name__}' (expected scalar)")
        return Vector(self.x * scalar, self.y * scalar)

    def magnitude(self) -> float:
        """Calculates the Euclidean magnitude (length) of the vector."""
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def __str__(self):
        return f"Vector({self.x}, {self.y}))"

    def __repr__(self):
        return f"Vector(x={self.x}, y={self.y}))"

if __name__ == "__main__":
    print("--- Day 6 Demonstrations ---")

    print("\n### Shape Hierarchy and Polymorphism (Problem 1.1) ###")
    shapes : list[Circle, Rectangle] = [Circle(5.5), Rectangle(3, 4)]
    for shape in shapes:
        # Printing string representation and both area and perimeter.
        print(f"The area of {shape}: {shape.area()}.")
        print(f"The perimeter of {shape}: {shape.perimeter()}.")

    print("\n### Vector Class with Dunder Methods (Problem 2.1) ###")
    vector1 = Vector(-1.5, 0)
    vector2 = Vector(10, 20)
    vector3 = Vector(0,0)

    print(f"vector1: {vector1}")
    print(f"vector2: {vector2}")

    # Demonstrate addition using +
    print(f"vector 1 + vector 2: {vector1 + vector2}.")
    # Demonstrate equality using ==
    print(f"vector 1 == vector 2: {vector1 == vector2}.")
    # Demonstrate scalar multiplication using *
    print(f"vector 1 == vector 2: {vector1 == vector2}.")
    # Attempt to add a Vector to a non-Vector (e.g., an int)
    try:
        Vector(3, 5) + 17
    except TypeError as e:
        print(f"Caught expected error: {e}.")
    
    try:
        vector1 * vector2
    except TypeError as e:
        print(f"Caught expected error: {e}.")

    try:
        vector3 == vector3.magnitude()
    except TypeError as e:
        print(f"Caught expected error: {e}.")

    # Try to instantiate an abstract shape (should raise TypeError)
    try:
        # generic_shape = Shape()
        print("Instantiated abstract Shape (this should not happen!)")
    except TypeError as e:
        print(f"Caught expected error: {e}")

# Test unsupported operations (TypeError)
    try:
        vector1 + "hello"
    except TypeError as e:
        print(f"Caught expected error: {e}")

    try:
        vector1 * vector2
    except TypeError as e:
        print(f"Caught expected error: {e}")

    try:
        vector1 == "not_a_vector"
    except TypeError: # This depends on how __eq__ is implemented; NotImplemented will return False
        print("Caught TypeError when comparing vector to non-vector (if __eq__ is strict)")
    print(f"vector1 == 'not_a_vector': {vector1 == 'not_a_vector'}") # If __eq__ returns NotImplemented, this will be False

    print("\n### BankAccount with File I/O (Problem 3.1) ###")
    # Make sure to delete or clear 'bank_transactions.log' before running multiple times for clean test
    my_logged_account = BankAccount("Alice Smith", 200.00)
    print(my_logged_account)
    try:
        my_logged_account.deposit(75.50)
        my_logged_account.withdraw(20.00)
        my_logged_account.withdraw(500.00) # Should raise InsufficientFundsError and NOT log
    except (InsufficientFundsError, InvalidAmountError) as e:
        print(f"Caught error in transaction: {e}")
    
    print(f"Check 'bank_transactions.log' file for entries.")