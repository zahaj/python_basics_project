from unittest.mock import Mock
from datetime import datetime

from mocking_basics import is_weekday

# Save a couple of test days
wednesday = datetime(year=2025, month=1, day=1)
sunday = datetime(year=2025, month=1, day=5)

datetime = Mock()

# Mock .today() to return Wednesday

datetime.today.return_value = wednesday
assert is_weekday()

datetime.today.return_value = sunday
assert is_weekday()
