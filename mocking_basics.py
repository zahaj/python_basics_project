from datetime import datetime
from unittest.mock import Mock
import unittest
import requests
from requests.exceptions import Timeout

# Save a couple of test days
wednesday = datetime(year=2025, month=1, day=1)
sunday = datetime(year=2025, month=1, day=5)

# Mock datetime to control today's date
datetime = Mock()

def is_weekday():
    today = datetime.today()
    # Python's datetime library treats Monday as 0 and Sunday as 6
    return (0 <= today.weekday() < 5)

# Mock .today() to return Wednesday
datetime.today.return_value = wednesday
assert is_weekday()

# Mock .today() to return Sunday
datetime.today.return_value = sunday
assert not is_weekday()

def get_holidays():
    r = requests.get("http://localhost/api/holidays")
    if r.status_code == 200:
        return r.json()
    return None

# Mock requests to mock its behaviour
requests = Mock()

def get_holidays():
    r = requests.get("http://localhost/api/holidays")
    if r.status_code == 200:
        return r.json()
    return None

class TestHolidays(unittest.TestCase):

    def test_get_holidays_timeout(self):
        # Test a connection timeout
        requests.get.side_effect = Timeout
        with self.assertRaises(Timeout):
            get_holidays()

if __name__ == "__main__":
    unittest.main()

