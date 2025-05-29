import unittest
import sys
from io import StringIO # To capture print output

# Import all necessary classes from oop_practice_modified.py file
from oop_practice_modified import Dog, Vector

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
        self.assertEquals(self.v1.x, -2)
        self.assertEquals(self.v1.y, 5.4)

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

# Standard boilerplate to run tests when the script is executed directly
if __name__ == '__main__':
    unittest.main()