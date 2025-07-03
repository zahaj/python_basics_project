import unittest
import sys
import json # New for testing JSON
from io import StringIO # To capture print output
from unittest.mock import patch, mock_open

# Import all necessary classes from oop_practice_modified.py file
from oop_practice_modified import(
    Dog,
    Vector,
    save_accounts_to_json,
    load_accounts_from_json,
    BankAccount, InsufficientFundsError, InvalidAmountError,
)

class TestDog(unittest.TestCase):

    def setUp(self):
        """
        Set up a fresh Dog object for each test method.
        This ensures tests are isolated and don't affect each other.
        """
        self.dog = Dog("Bobby", "Spaniel", 10)
    
    # --- Test __init__ method ---
    def test_valid_dog_initialization(self):
        """Test if the initialization with valid arguments is correct."""
        self.assertEqual(self.dog.name, "Bobby")
        self.assertEqual(self.dog.breed, "Spaniel")
        self.assertEqual(self.dog.age, 10)

    def test_init_with_invalid_name_raises_error(self):
        """Test if the initialization with invalid name raises ValueError."""
        with self.assertRaises(ValueError):
            Dog("", "Spaniel", 5)
        with self.assertRaises(ValueError):
            Dog([1, 2, 3], "Poodle", 1)

    def test_init_with_invalid_breed_raises_error(self):
        """Test if the initialization with invalid breed raises ValueError."""
        with self.assertRaises(ValueError):
            Dog("Max", True, 9)
        with self.assertRaises(ValueError):
            Dog("Max", "", 1)

    def test_init_with_invalid_age_raises_error(self):
        """Test if the initialization with invalid age raises ValueError."""
        with self.assertRaises(ValueError):
            Dog("Jimmy", "Labradoodle", 3.5)
        with self.assertRaises(ValueError):
            Dog("Jimmy", "Labradoodle", -6)
        with self.assertRaises(ValueError):
            Dog("Jimmy", "Labradoodle", "5")
    
# Test property age getter and setter 
    def test_age_property_getter(self):
        """Test if property age returns the correct value."""
        self.assertEqual(self.dog.age, 10)

    def test_age_property_setter_valid_new_age(self):
        """Test if setting valid new age works correctly."""
        self.dog.age = 11
        self.assertEqual(self.dog.age, 11)

    def test_age_property_setter_non_integer_new_age(self):
        """
        Test if setting non-integer new age raises ValueError and check if
        age does not change on error.
        """
        initial_age = self.dog.age
        with self.assertRaises(ValueError):
            self.dog.age = "11"
        self.assertEqual(self.dog.age, initial_age) # Age should remain unchanged

    def test_age_property_setter_negative_new_age(self):
        """
        Test if setting negative new age raises ValueError and check if
        age does not change on error.
        """
        initial_age = self.dog.age
        with self.assertRaises(ValueError):
            self.dog.age = -1
        self.assertEqual(self.dog.age, initial_age) # Age should remain unchanged

    def test_bark_output(self):
        """Test if bark() prints the correct output."""
        # Capture stdout to test what's printed
        captured_output = StringIO()
        sys.stdout = captured_output # Redirect stdout
        self.dog.bark()
        sys.stdout = sys.__stdout__ # Reset redirect
        self.assertEqual(captured_output.getvalue().strip(), f"{self.dog.name} says Woof!")

class TestVector(unittest.TestCase):

    def setUp(self):
        """
        Set up a fresh Vector object for each test method.
        This ensures tests are isolated and don't affect each other.
        """
        self.v1 = Vector(-2, 5.4)
        self.v2 = Vector(1, 2)
        self.v3 = Vector(-2, 5.4) # For equality test
    
    # Test __init__ method
    def test_valid_coordinates_initialization(self):
        self.assertEqual(self.v1.x, -2)
        self.assertEqual(self.v1.y, 5.4)

    def test_init_non_numeric_coordinates_raises_error(self):
        with self.assertRaises(TypeError):
            Vector("1", 2)
        with self.assertRaises(TypeError):
            Vector(1, True)

    # Test dunder methods
    # Test __add__
    def test_vector_addition(self):
        v_sum = self.v1 + self.v2
        self.assertEqual(v_sum.x, -1)
        self.assertEqual(v_sum.y, 7.4)
        self.assertEqual(v_sum, Vector(-1, 7.4))

    def test_vector_addition_non_vector_raises_error(self):
        with self.assertRaises(TypeError):
            self.v1 + 5
        with self.assertRaises(TypeError):
            self.v1 + "vector"

    # Test __eq__
    def test_vector_equality(self):
        """Test equality (==) for identical vectors."""
        self.assertTrue(self.v1 == self.v3)
        self.assertFalse(self.v1 == self.v2)

    # It's generally more robust to test the equality (__eq__) of your object with a non-matching type.
    def test_vector_equality_with_non_vector(self):
        """Test comparison with non-Vector for equality (should be False)."""
        # self.v1.__eq__("not a vector") will return NotImplemented, leading to False for ==
        self.assertFalse(self.v1 == "not a vector")
        self.assertFalse(self.v1 == None)

    # Test __ne__
    def test_vector_inequality(self):
        """Test inequality (!=) for different vectors."""
        self.assertTrue(self.v1 != self.v2)
        self.assertFalse(self.v1 != self.v3)

    # Test __mul__
    def test_vector_multiplication(self):
        v1_scaled = self.v1 * 2
        self.assertEqual(v1_scaled, Vector(-4, 10.8))

        v2_scaled_float = self.v2 * 1.5
        self.assertEqual(v2_scaled_float.x, 1.5)
        self.assertEqual(v2_scaled_float.y, 3.0)
        self.assertEqual(v2_scaled_float, Vector(1.5, 3.0))

    def test_vector_multiplication_non_scalar_raises_error(self):
        with self.assertRaises(TypeError):
            self.v1 * self.v2
        with self.assertRaises(TypeError):
            self.v1 * "scalar"  

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
        self.expected_json_string = json.dumps(self.expected_json_data, indent=4, ensure_ascii=False)

    @patch("builtins.open", new_callable=mock_open) # Decorator version
    def test_save_accounts_writes_correct_json(self, mock_file_open):
        """Test that save_accounts_to_json correctly writes account data as JSON."""
        save_accounts_to_json(self.accounts, self.filename)

        # 1. Assert 'open' was called with the correct arguments
        mock_file_open.assert_called_once_with(self.filename, 'w', encoding='utf-8')

        # 2. Assert 'write' was called with the correct JSON content
        # mock_file_open() is the mock file handle returned by mock_open
        # .write.call_args[0][0] gets the first argument of the first call to .write
        written_content_parts = [call.args[0] for call in mock_file_open().write.call_args_list]
        written_content = "".join(written_content_parts) # Join all parts into a single string

        # Use json.loads to compare the actual written JSON with the expected JSON structure
        self.assertEqual(json.loads(written_content), self.expected_json_data)
        # Or, compare the formatted string directly if you want to be strict about formatting
        self.assertEqual(written_content, self.expected_json_string)

    @patch("builtins.open", new_callable=mock_open)
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

    @patch("builtins.open", side_effect=FileNotFoundError)
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


    @patch("builtins.open", new_callable=mock_open)
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

    @patch("builtins.open", new_callable=mock_open)
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
        self.assertIn("Error: 'balance'", captured_output.getvalue()) # Specific error check

    @patch("builtins.open", new_callable=mock_open)
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
    unittest.main()