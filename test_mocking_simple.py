import unittest
from unittest.mock import patch

from mocking_simple import perform_calculation, add_one_and_double

class TestCalculations(unittest.TestCase):

    def test_perform_calculation_with_mocked_helper(self):
        