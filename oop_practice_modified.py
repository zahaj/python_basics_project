# Day 5: Advanced OOP & Testing Basics

from typing import List, Union, Any, Optional

class InsufficientFundsError(Exception):
    """Raised when a bank account withdrawal is attempted with insufficient funds."""
    pass

class InvalidAmountError(Exception):
    """Raised when a deposit or withdrawal amount is zero, negative, or non-numeric."""
    pass

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

    def withdraw(self, amount: float):
        if not isinstance(amount, (float, int)) or amount <= 0:
            raise InvalidAmountError("Withdraw amount must be a positive number.")
            # return # Not necessary anymore - raise already stops execution
        if amount > self._balance:
            raise InsufficientFundsError("Cannot withdraw: Not enough money in the account.")
        else:
            self._balance -= amount
            print(f"Withdrew ${amount:.2f}. New balance: ${self._balance:.2f}")

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
    def age(self, new_age: int):
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

