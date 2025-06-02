import unittest
from unittest.mock import patch, MagicMock

from report_generator_improved import _fetch_raw_data, _format_data_for_display, ReportGenerator

class TestReportGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = ReportGenerator()

    @patch('report_generator_improved._fetch_raw_data')
    def test_generate_report_with_user_data(self, mock_fetch_raw_data):
        mock_fetch_raw_data.return_value = [
            {"id": 10, "name": "Eva"},
            {"id": 12, "name": "Jack"}
        ]

        result = self.generator.generate_report("id")
        expected_result = expected_result = (
            "--- Report for id ---\n"  # This should be "id" because that's your source_id
            "User ID: 10, Name: Eva\n" # This should be Eva's data
            "User ID: 12, Name: Jack\n" # This should be Jack's data
            "--- End Report ---"
        )
        self.assertEqual(result, expected_result)
        mock_fetch_raw_data.assert_called_once()


    @patch('report_generator_improved._fetch_raw_data')
    def test_generate_report_with_no_data(self, mock_fetch_raw_data):
        mock_fetch_raw_data.return_value = []
        result = self.generator.generate_report("id")
        expected_result = (
            "--- Report for id ---\n"
            "No items to display.\n"
            "--- End Report ---"
        )
        self.assertEqual(result, expected_result)
        mock_fetch_raw_data.assert_called_once_with("id")

    @patch('report_generator_improved._fetch_raw_data')
    def test_generate_report_raises_on_fetch_error(self, mock_fetch_raw_data):
        mock_fetch_raw_data.side_effect = ValueError("Simulated fetch error")
        with self.assertRaises(ValueError):
            self.generator.generate_report("id")

    @patch('report_generator_improved._format_data_for_display')
    @patch('report_generator_improved._fetch_raw_data')
    def test_generate_report_uses_formatter_correctly(self, mock_fetch_raw_data, mock_format_data_for_display):
        mock_fetch_raw_data.return_value = [{"id": 1, "data": "X"}]
        mock_format_data_for_display.return_value= "MOCKED FORMATTED STRING"
        result = self.generator.generate_report("id")
        expected_result = (
            "--- Report for id ---\n"
            "MOCKED FORMATTED STRING\n"
            "--- End Report ---"
        )
        mock_format_data_for_display.assert_called_once()
        mock_format_data_for_display.assert_called_once_with([{"id": 1, "data": "X"}])
        self.assertEqual(result, expected_result)
        