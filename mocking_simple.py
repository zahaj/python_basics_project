# my_operations.py

def add_one_and_double(number: int) -> int:
    """
    A helper function: Adds one to a number and then doubles the result.
    """
    print(f"(Helper: add_one_and_double called with {number})") # Added print to show when real helper runs
    return (number + 1) * 2

def perform_calculation(value: int) -> int:
    """
    Performs a calculation using the add_one_and_double helper.
    """
    print(f"Performing main calculation for value: {value}")
    intermediate_result = add_one_and_double(value) # This is the dependency we might mock
    final_result = intermediate_result + 5
    print(f"Main calculation finished. Final result: {final_result}")
    return final_result

class PaymentGateway:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.is_connected = False # Simulates connection status
    def connect(self) -> bool:
        print(f"Connecting to payment gateway with key: {self.api_key}...")
        self.is_connected = True
        return True
    def process_payment(self, amount: float, token: str) -> str:
        if not self.is_connected:
            raise ConnectionError("Gateway not connected.")
        print(f"Processing ${amount:.2f} with token {token}...")
        return f"SUCCESS_{token}_${amount:.2f}"    
    def handle_purchase(gateway: PaymentGateway, product_price: float, user_payment_token: str) -> str:
        gateway.connect()
        result = gateway.process_payment(product_price, user_payment_token)
        return result

def _apply_operation(num: int) -> int:
    print(f" (Real helper: _apply_operation called with {num})")
    return num * 2

def calculate_complex_value(initial_value: int) -> int:
    first_result = _apply_operation(initial_value)
    second_result = _apply_operation(first_result + 1)
    print(f" (Main function: calculate_complex_value processing {initial_value})")
    return second_result + 5

if __name__ == "__main__":
    print("--- Demonstrating my_operations directly ---")
    # When run directly, the actual helper function is called
    result = perform_calculation(5)
    print(f"Direct run result: {result}") # Expected: ((5+1)*2) + 5 = 12 + 5 = 17