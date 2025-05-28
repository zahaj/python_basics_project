from abc import ABC, abstractmethod
import random
from typing import List

# 4.1 PaymentProcessor ABC

class PaymentProcessor(ABC):
    """
    Abstract Base Class for payment processing.
    Defines a contract for all concrete payment processor implementations.
    """

    @abstractmethod
    def process_payment(self, amount: float) -> str:
        """
        Processes a payment of the given amount.
        Must be implemented by subclasses.

        Args:
            amount (float): The amount to process.

        Returns:
            str: A unique transaction ID.
        """
        pass 
    @abstractmethod
    def get_processor_name(self) -> str:
        """
        Returns the name of the payment processor.
        Must be implemented by subclasses.
        """
        pass

# Concrete Subclasses

class CreditCardProcessor(PaymentProcessor):

    def __init__(self, api_key: str):
        if not isinstance(api_key, str) or not api_key.strip():
            raise ValueError(f"API key must be a non-empty string.")
        self.api_key = api_key
        print(f"CreditCardProcessor initialized with API Key: {self.api_key[:4]}...")


    def process_payment(self, amount: float) -> str:
        if not isinstance(amount, (int, float)) or amount <=0:
            raise ValueError(f"Payment amount must be positive.")
        
        # Simulate payment processing
        transaction_id = f"CC_{amount:.2f}_{self.api_key[:4]}_{random.randint(10000, 99999)}"
        print(f"Processing ${amount:.2f} via Credit Card. Transaction ID: {transaction_id}")
        return transaction_id

    def get_processor_name(self) -> str:
        return "Credit Card Processor"
    
    def __str__(self):
        return f"CreditCardProcessor(API Key: {self.api_key[:4]}...)"
    
    def __repr__(self):
        return f"CreditCardProcessor(api_key='{self.api_key}')"
    
class PayPalProcessor(PaymentProcessor):

    def __init__(self, username: str):
        if not isinstance(username, str) or not username.strip():
            raise TypeError("PayPal username must be a non-empty string.")
        self.username = username
        print(f"PayPalProcessor initialized for user: {self.username}")

    def process_payment(self, amount: float):
        if not isinstance(amount, float) or amount <=0:
            raise ValueError(f"Pauyment amount must be positive.")

        # Simulate payment processing
        transaction_id = f"PP_{amount:.2f}_{self.username[:4]}_{random.randint(10000, 99999)}"
        print(f"Processing ${amount:.2f} via PayPal. Transaction ID: {transaction_id}")
        return transaction_id
    
    def get_processor_name(self):
        return "PayPal Processor"
    
    def __str__(self):
        return f"PayPalProcessor(Username: {self.username})"
    
    def __repr__(self):
        return f"PayPalProcessor(username='{self.username}')"
    
# --- Demonstration Section for payment_processors.py ---
if __name__ == "__main__":
    print("--- Abstract Base Classes (ABCs) Demonstration (Problem 4.1) ---")

    # Create instances of concrete processors
    cc_processor = CreditCardProcessor("sk_live_abc123xyz789")
    pp_processor = PayPalProcessor("john.cleese@example.com")
    
    # Put them in a list, treating them polymorphically as PaymentProcessor
    processors: List[PaymentProcessor] = [cc_processor, pp_processor]

    for processor in processors:
        print(f"\n--- Using {processor.get_processor_name()} ---")
        try:
            transaction_id = processor.process_payment(random.uniform(25.0, 150.0))
            print(f"Successfully processed. Received ID: {transaction_id}")
        except ValueError as e:
            print(f"Error processing payment: {e}")

    print("\n--- Attempting to instantiate the abstract class ---")
    try:
        # This will raise a TypeError because PaymentProcessor is an ABC
        generic_processor = PaymentProcessor()
        # TypeError: Can't instantiate abstract class PaymentProcessor with abstract methods get_processor_name, process_payment
        print("Instantiated PaymentProcessor (this should not happen!)")
    except TypeError as e:
        print(f"Caught expected error: {e}")

    print("\n--- Demonstrating required implementation ---")
    # This class would raise a TypeError because it doesn't implement all abstract methods
    
    class IncompleteProcessor(PaymentProcessor):
        def process_payment(self, amount: float) -> str:
            return "dummy"
    
    try:
        incomplete = IncompleteProcessor()
    except TypeError as e:
        print(f"Caught expected error for incomplete implementation: {e}")
