import unittest
from unittest.mock import MagicMock, patch

from report_generator import _format_data_for_display

class TestReportGenerator(unittest.TestCase):
    
    def setUp(self):
        self.generator = ReportGenerator()

    @patch("report_generator._fetch_raw_data") # replaces _fetch_raw_data only inside this test
    def test_format_data_for_display_with_mocked_name(self, mock_function_fetch_raw_data):
        mock_function_fetch_raw_data.return_value = [
            {"id": 10, "name": "Eva"},
            {"id": 12, "name": "Jack"}
        ]
        result = _format_data_for_display("users")
        expected_result = "User ID: 10, Name: Eva\nUser ID: 12, Name: Jack"
        self.assertEqual(result, expected_result)

        mock_function_fetch_raw_data.assert_called_once_with("users")

    @patch("report_generator._fetch_raw_data") # replaces _fetch_raw_data only inside this test
    def test_format_data_for_display_with_item(self, mock_function_fetch_raw_data):
        mock_function_fetch_raw_data.return_value = [
            {"id": 71, "item": "Brick"},
            {"id": 72, "item": "House"}
        ]
        result = _format_data_for_display("products")
        expected_result = "Product ID: 71, Item: Brick\nProduct ID: 72, Item: House"

        self.assertEqual(result, expected_result)
        mock_function_fetch_raw_data.assert_called_once_with("products")

    @patch("report_generator._fetch_raw_data") # replaces _fetch_raw_data only inside this test
    def test_format_data_for_display_with_empty_list(self, mock_function_fetch_raw_data):
        mock_function_fetch_raw_data.return_value = []
        result = _format_data_for_display("unknown")
        expected_result = ""

        self.assertEqual(result, expected_result)
        mock_function_fetch_raw_data.assert_called_once_with("unknown")

    if __name__ == "__main__":
        unittest.main()