import unittest
from oop_practice_modified import BankAccount, InsufficientFundsError, InvalidAmountError

class TestBankAccount(unittest.TestCase):
    # Your test methods will go here
    def setUp(self):
        """
        Set up a fresh BankAccount object for each test method.
        This ensures tests are isolated and don't affect each other.
        """
        self.account = BankAccount("Test User", 100.00)

    def tearDown(self):
        """
        Clean up after each test method (optional, but good practice).
        Not strictly necessary for this simple case, but useful for file I/O, DB connections, etc.
        """
        print(f"--- Tearing down after {self._testMethodName} ---")
        # No specific cleanup needed for BankAccount
        pass

   # --- Test __init__ method ---
    def test_initial_balance_set_correctly(self):
        """Test if the initial balance is set correctly."""
        self.assertEqual(self.account.balance, 100.00) # Accessing via property

    def test_initial_balance_default_to_zero(self):
        """Test if initial balance defaults to 0.00 if not provided."""
        default_account = BankAccount("Default User")
        self.assertEqual(default_account.balance, 0.00)

    def test_init_with_invalid_account_holder(self):
        """Test __init__ raises ValueError for invalid account holder name."""
        with self.assertRaises(ValueError):
            BankAccount("", 100.00)
        with self.assertRaises(ValueError):
            BankAccount(123, 100.00)

    def test_init_with_negative_initial_balance(self):
        """Test __init__ raises ValueError for negative initial balance."""
        with self.assertRaises(ValueError):
            BankAccount("Test User", -50.00)

    # --- Test deposit method ---
    def test_deposit_positive_amount(self):
        """Test successful deposit of a positive amount."""
        self.account.deposit(50.00)
        self.assertEqual(self.account.balance, 150.00)

    def test_deposit_zero_amount_raises_error(self):
        """Test deposit raises InvalidAmountError for zero amount."""
        initial_balance = self.account.balance
        with self.assertRaises(InvalidAmountError):
            self.account.deposit(0)
        # Ensure balance doesn't change on error
        self.assertEqual(self.account.balance, initial_balance)

    def test_deposit_negative_amount_raises_error(self):
        """Test deposit raises InvalidAmountError for negative amount."""
        initial_balance = self.account.balance
        with self.assertRaises(InvalidAmountError):
            self.account.deposit(-20.00)
        self.assertEqual(self.account.balance, initial_balance)

    def test_deposit_non_numeric_amount_raises_error(self):
        """Test deposit raises InvalidAmountError for non-numeric amount."""
        initial_balance = self.account.balance
        with self.assertRaises(InvalidAmountError):
            self.account.deposit("abc")
        self.assertEqual(self.account.balance, initial_balance)

    # --- Test withdraw method ---
    def test_withdraw_sufficient_funds(self):
        """Test successful withdrawal with sufficient funds."""
        self.account.withdraw(50.00)
        self.assertEqual(self.account.balance, 50.00)

    def test_withdraw_all_funds(self):
        """Test withdrawal of the entire balance."""
        self.account.withdraw(100.00)
        self.assertEqual(self.account.balance, 0.00)

    def test_withdraw_insufficient_funds_raises_error(self):
        """Test withdraw raises InsufficientFundsError when funds are low."""
        initial_balance = self.account.balance
        with self.assertRaises(InsufficientFundsError):
            self.account.withdraw(200.00) # Trying to withdraw more than available
        self.assertEqual(self.account.balance, initial_balance) # Balance should be unchanged

    def test_withdraw_zero_amount_raises_error(self):
        """Test withdraw raises InvalidAmountError for zero amount."""
        initial_balance = self.account.balance
        with self.assertRaises(InvalidAmountError):
            self.account.withdraw(0)
        self.assertEqual(self.account.balance, initial_balance)

    def test_withdraw_negative_amount_raises_error(self):
        """Test withdraw raises InvalidAmountError for negative amount."""
        initial_balance = self.account.balance
        with self.assertRaises(InvalidAmountError):
            self.account.withdraw(-20.00)
        self.assertEqual(self.account.balance, initial_balance)

    def test_withdraw_non_numeric_amount_raises_error(self):
        """Test withdraw raises InvalidAmountError for non-numeric amount."""
        initial_balance = self.account.balance
        with self.assertRaises(InvalidAmountError):
            self.account.withdraw("xyz")
        self.assertEqual(self.account.balance, initial_balance)

    # --- Test balance property (read-only) ---
    def test_balance_is_read_only_property(self):
        """Test that direct assignment to balance raises AttributeError."""
        with self.assertRaises(AttributeError):
            self.account.balance = 500.00


# Standard boilerplate to run tests when the script is executed directly
if __name__ == '__main__':
    unittest.main()