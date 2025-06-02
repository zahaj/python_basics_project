import unittest
import sys
import json # New for testing JSON
from io import StringIO
from unittest.mock import patch, mock_open # New for Day 7 (Problem 3.1)

# Import all necessary classes and functions from your oop_practice.py file
from oop_practice import (
    BankAccount, InsufficientFundsError, InvalidAmountError,
    Dog, Vector,
    Shape, Circle, Rectangle,
    save_accounts_to_json, load_accounts_from_json # New imports for Day 7
)

# --- Test BankAccount Class (from Day 5 - provided previously, included for context) ---
class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount("Test User", 100.00)

    def test_initial_balance_set_correctly(self):
        self.assertEqual(self.account.balance, 100.00)

    def test_initial_balance_default_to_zero(self):
        default_account = BankAccount("Default User")
        self.assertEqual(default_account.balance, 0.00)

    def test_init_with_invalid_account_holder(self):
        with self.assertRaises(ValueError):
            BankAccount("", 100.00)
        with self.assertRaises(ValueError):
            BankAccount(123, 100.00)

    def test_init_with_negative_initial_balance(self):
        with self.assertRaises(ValueError):
            BankAccount("Test User", -50.00)

    def test_deposit_positive_amount(self):
        self.account.deposit(50.00)
        self.assertEqual(self.account.balance, 150.00)

    def test_deposit_zero_amount_raises_error(self):
        initial_balance = self.account.balance
        with self.assertRaises(InvalidAmountError):
            self.account.deposit(0)
        self.assertEqual(self.account.balance, initial_balance)

    def test_deposit_negative_amount_raises_error(self):
        initial_balance = self.account.balance
        with self.assertRaises(InvalidAmountError):
            self.account.deposit(-20.00)
        self.assertEqual(self.account.balance, initial_balance)

    def test_deposit_non_numeric_amount_raises_error(self):
        initial_balance = self.account.balance
        with self.assertRaises(InvalidAmountError):
            self.account.deposit("abc")
        self.assertEqual(self.account.balance, initial_balance)

    def test_withdraw_sufficient_funds(self):
        self.account.withdraw(50.00)
        self.assertEqual(self.account.balance, 50.00)

    def test_withdraw_all_funds(self):
        self.account.withdraw(100.00)
        self.assertEqual(self.account.balance, 0.00)

    def test_withdraw_insufficient_funds_raises_error(self):
        initial_balance = self.account.balance
        with self.assertRaises(InsufficientFundsError):
            self.account.withdraw(200.00)
        self.assertEqual(self.account.balance, initial_balance)

    def test_withdraw_zero_amount_raises_error(self):
        initial_balance = self.account.balance
        with self.assertRaises(InvalidAmountError):
            self.account.withdraw(0)
        self.assertEqual(self.account.balance, initial_balance)

    def test_withdraw_negative_amount_raises_error(self):
        initial_balance = self.account.balance
        with self.assertRaises(InvalidAmountError):
            self.account.withdraw(-20.00)
        self.assertEqual(self.account.balance, initial_age)

    def test_withdraw_non_numeric_amount_raises_error(self):
        initial_balance = self.account.balance
        with self.assertRaises(InvalidAmountError):
            self.account.withdraw("xyz")
        self.assertEqual(self.account.balance, initial_balance)

    def test_balance_is_read_only_property(self):
        with self.assertRaises(AttributeError):
            self.account.balance = 500.00

    def test_bank_account_equality(self): # Added for Problem 2.1 to make testing easier
        acc1 = BankAccount("Test User", 100.00)
        acc2 = BankAccount("Test User", 100.00)
        acc3 = BankAccount("Another User", 100.00)
        acc4 = BankAccount("Test User", 200.00)

        self.assertEqual(acc1, acc2)
        self.assertNotEqual(acc1, acc3)
        self.assertNotEqual(acc1, acc4)
        self.assertFalse(acc1 == "not an account")
        self.assertFalse(acc1 == None)


# --- Test Dog Class (from Day 6) ---
class TestDog(unittest.TestCase):
    def setUp(self):
        self.dog = Dog("Buddy", "Golden Retriever", 5)

    def test_dog_initialization(self):
        self.assertEqual(self.dog.name, "Buddy")
        self.assertEqual(self.dog.breed, "Golden Retriever")
        self.assertEqual(self.dog.age, 5)

    def test_init_invalid_name(self):
        with self.assertRaises(ValueError):
            Dog("", "Poodle", 3)
        with self.assertRaises(ValueError):
            Dog(123, "Poodle", 3)

    def test_init_invalid_breed(self):
        with self.assertRaises(ValueError):
            Dog("Max", "", 3)
        with self.assertRaises(ValueError):
            Dog("Max", None, 3)

    def test_age_property_getter(self):
        self.assertEqual(self.dog.age, 5)

    def test_age_property_setter_valid(self):
        self.dog.age = 7
        self.assertEqual(self.dog.age, 7)

    def test_age_property_setter_negative_age(self):
        initial_age = self.dog.age
        with self.assertRaises(ValueError):
            self.dog.age = -1
        self.assertEqual(self.dog.age, initial_age) # Age should remain unchanged

    def test_age_property_setter_non_integer_age(self):
        initial_age = self.dog.age
        with self.assertRaises(ValueError):
            self.dog.age = 5.5
        self.assertEqual(self.dog.age, initial_age) # Age should remain unchanged

    def test_bark_output(self):
        # Capture stdout to test what's printed
        captured_output = StringIO()
        sys.stdout = captured_output # Redirect stdout
        self.dog.bark()
        sys.stdout = sys.__stdout__ # Reset redirect
        self.assertEqual(captured_output.getvalue().strip(), f"{self.dog.name} says Woof!")


# --- Test Vector Class (from Day 6) ---
class TestVector(unittest.TestCase):
    def setUp(self):
        self.v1 = Vector(3, 4)
        self.v2 = Vector(1, 2)
        self.v3 = Vector(3, 4) # For equality test

    def test_vector_initialization(self):
        self.assertEqual(self.v1.x, 3)
        self.assertEqual(self.v1.y, 4)

    def test_init_non_numeric_coordinates_raises_error(self):
        with self.assertRaises(TypeError):
            Vector("a", 1)
        with self.assertRaises(TypeError):
            Vector(1, "b")

    def test_init_boolean_coordinates_raises_error(self): # Added specific test for boolean
        with self.assertRaises(TypeError):
            Vector(1, True)
        with self.assertRaises(TypeError):
            Vector(False, 1)

    def test_vector_addition(self):
        v_sum = self.v1 + self.v2
        self.assertEqual(v_sum.x, 4)
        self.assertEqual(v_sum.y, 6)
        self.assertEqual(v_sum, Vector(4, 6)) # Using __eq__

    def test_vector_addition_type_error(self):
        with self.assertRaises(TypeError):
            self.v1 + 5
        with self.assertRaises(TypeError):
            self.v1 + "vector"

    def test_vector_subtraction(self):
        v_diff = self.v1 - self.v2
        self.assertEqual(v_diff.x, 2)
        self.assertEqual(v_diff.y, 2)
        self.assertEqual(v_diff, Vector(2, 2))

    def test_vector_subtraction_type_error(self):
        with self.assertRaises(TypeError):
            self.v1 - 5

    def test_vector_equality(self):
        self.assertTrue(self.v1 == self.v3)
        self.assertFalse(self.v1 == self.v2)
        # Test comparison with non-Vector (should evaluate to False)
        self.assertFalse(self.v1 == "not a vector")
        self.assertFalse(self.v1 == None)

    def test_vector_inequality(self):
        self.assertTrue(self.v1 != self.v2)
        self.assertFalse(self.v1 != self.v3)
        # Test comparison with non-Vector (should evaluate to True)
        self.assertTrue(self.v1 != "not a vector")
        self.assertTrue(self.v1 != None)

    def test_vector_scalar_multiplication(self):
        v_scaled = self.v1 * 2
        self.assertEqual(v_scaled.x, 6)
        self.assertEqual(v_scaled.y, 8)
        self.assertEqual(v_scaled, Vector(6, 8))

        v_scaled_float = self.v2 * 1.5
        self.assertEqual(v_scaled_float.x, 1.5)
        self.assertEqual(v_scaled_float.y, 3.0)
        self.assertEqual(v_scaled_float, Vector(1.5, 3.0))

    def test_vector_reverse_scalar_multiplication(self):
        v_scaled = 2 * self.v1
        self.assertEqual(v_scaled, Vector(6, 8))

    def test_vector_scalar_multiplication_type_error(self):
        with self.assertRaises(TypeError):
            self.v1 * self.v2 # Vector by Vector
        with self.assertRaises(TypeError):
            self.v1 * "scalar"

    def test_vector_magnitude(self):
        self.assertEqual(self.v1.magnitude(), 5.0) # sqrt(3^2 + 4^2) = 5
        self.assertAlmostEqual(Vector(1, 1).magnitude(), math.sqrt(2))


# --- Test Account Persistence (Problem 3.1) ---
class TestAccountPersistence(unittest.TestCase):
    def setUp(self):
        self.accounts = [
            BankAccount("Alice", 100.0),
            BankAccount("Bob", 200.0)
        ]
        self.filename = 'test_accounts.json'
        self.expected_json_data = [
            {"account_holder": "Alice", "balance": 100.0},
            {"account_holder": "Bob", "balance": 200.0}
        ]
        self.expected_json_string = json.dumps(self.expected_json_data, indent=4, ensure_ascii=False) + "\n" # json.dump adds a newline by default


    @patch('builtins.open', new_callable=mock_open)
    def test_load_accounts_reads_correct_json(self, mock_file_open):
        """Test that load_accounts_from_json correctly reads and reconstructs accounts."""
        # Arrange: Set the content that the mock file should 'read'
        mock_file_open.return_value.read.return_value = self.expected_json_string

        # Act: Call the function under test
        loaded_accounts = load_accounts_from_json(self.filename)

        # Assert:
        # 1. Assert 'open' was called with the correct arguments
        mock_file_open.assert_called_once_with(self.filename, 'r', encoding='utf-8')

        # 2. Assert the number of accounts loaded
        self.assertEqual(len(loaded_accounts), len(self.accounts))

        # 3. Assert the properties of the loaded accounts (using BankAccount's __eq__)
        self.assertEqual(loaded_accounts[0], self.accounts[0])
        self.assertEqual(loaded_accounts[1], self.accounts[1])


    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_accounts_handles_file_not_found(self, mock_file_open):
        """Test that load_accounts_from_json handles FileNotFoundError."""
        # Capture print output to ensure the warning message is displayed
        captured_output = StringIO()
        sys.stdout = captured_output
        
        loaded_accounts = load_accounts_from_json("non_existent.json")
        
        sys.stdout = sys.__stdout__ # Reset stdout
        
        self.assertEqual(loaded_accounts, []) # Should return an empty list
        self.assertIn("WARNING: File 'non_existent.json' not found.", captured_output.getvalue())
        mock_file_open.assert_called_once_with("non_existent.json", 'r', encoding='utf-8')


    @patch('builtins.open', new_callable=mock_open)
    def test_load_accounts_handles_invalid_json(self, mock_file_open):
        """Test that load_accounts_from_json handles invalid JSON format."""
        # Arrange: Make the mock file return invalid JSON content
        mock_file_open.return_value.read.return_value = "{'bad_json': "

        # Capture print output
        captured_output = StringIO()
        sys.stdout = captured_output
        
        loaded_accounts = load_accounts_from_json(self.filename)
        
        sys.stdout = sys.__stdout__ # Reset stdout
        
        self.assertEqual(loaded_accounts, []) # Should return an empty list
        self.assertIn("ERROR: Invalid JSON format in", captured_output.getvalue())
        mock_file_open.assert_called_once_with(self.filename, 'r', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open)
    def test_load_accounts_handles_invalid_json_entry_format(self, mock_file_open):
        """Test that load_accounts_from_json handles valid JSON but invalid account entry format."""
        # Arrange: JSON is valid, but an account entry is missing a key or has wrong type
        invalid_json_string = json.dumps([
            {"account_holder": "Valid", "balance": 100.0},
            {"account_holder": "Invalid Account"} # Missing 'balance'
        ], indent=4)
        mock_file_open.return_value.read.return_value = invalid_json_string

        captured_output = StringIO()
        sys.stdout = captured_output
        
        loaded_accounts = load_accounts_from_json(self.filename)
        
        sys.stdout = sys.__stdout__ # Reset stdout
        
        self.assertEqual(len(loaded_accounts), 1) # Only one account should be loaded
        self.assertEqual(loaded_accounts[0].account_holder, "Valid")
        self.assertIn("WARNING: Skipping invalid account entry from JSON", captured_output.getvalue())
        self.assertIn("KeyError: 'balance'", captured_output.getvalue()) # Specific error check

    @patch('builtins.open', new_callable=mock_open)
    def test_load_accounts_handles_json_not_list(self, mock_file_open):
        """Test that load_accounts_from_json handles JSON data that is not a list."""
        mock_file_open.return_value.read.return_value = json.dumps({"single_account": {"account_holder": "Test", "balance": 50}})
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        loaded_accounts = load_accounts_from_json(self.filename)
        
        sys.stdout = sys.__stdout__
        
        self.assertEqual(loaded_accounts, [])
        self.assertIn("WARNING: JSON file", captured_output.getvalue())
        self.assertIn("does not contain a list", captured_output.getvalue())


# Standard boilerplate to run tests when the script is executed directly
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False) # exit=False allows other code to run after tests
