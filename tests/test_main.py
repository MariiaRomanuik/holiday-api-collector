import unittest
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime
import json
from main import (
    HolidayCollector,
    HolidaySaver,
    HolidayProcessor
)


class TestHolidayCollector(unittest.TestCase):

    @patch('requests.get')
    def test_fetch_holidays(self, mock_get):
        # Mock response data
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": {
                "holidays": [
                    {"name": "Mock Holiday 1", "date": "1992-07-07"},
                    {"name": "Mock Holiday 2", "date": "1992-07-08"}
                ]
            }
        }
        mock_get.return_value = mock_response

        collector = HolidayCollector(api_key='fake_api_key')
        start_date = datetime(year=1992, month=7, day=7)
        end_date = datetime(year=1992, month=9, day=18)

        holidays = collector.fetch_holidays('us', start_date, end_date)

        self.assertEqual(len(holidays), 2)
        self.assertEqual(holidays[0]['name'], 'Mock Holiday 1')
        self.assertEqual(holidays[1]['name'], 'Mock Holiday 2')
        mock_get.assert_called_once()


class TestHolidaySaver(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    def test_save_holidays(self, mock_open_func):
        saver = HolidaySaver()
        holidays = [
            {"name": "Mock Holiday 1", "date": "1992-07-07"},
            {"name": "Mock Holiday 2", "date": "1992-07-08"}
        ]
        start_date = datetime(year=1992, month=7, day=7)
        end_date = datetime(year=1992, month=9, day=18)

        saver.save_holidays('us', holidays, start_date, end_date)

        mock_open_func.assert_called_once_with('output_files\\us_07-07-1992_18-09-1992.txt', 'w')
        mock_open_func().write.assert_any_call(json.dumps(holidays[0]) + "\n")
        mock_open_func().write.assert_any_call(json.dumps(holidays[1]) + "\n")


class TestHolidayProcessor(unittest.TestCase):

    @patch.object(HolidayCollector, 'fetch_holidays', return_value=[
        {"name": "Mock Holiday 1", "date": "1992-07-07"},
        {"name": "Mock Holiday 2", "date": "1992-07-08"}
    ])
    @patch.object(HolidaySaver, 'save_holidays')
    def test_process_holidays(self, mock_save_holidays, mock_fetch_holidays):
        processor = HolidayProcessor(api_key='fake_api_key')
        start_date = datetime(year=1992, month=7, day=7)
        end_date = datetime(year=1992, month=9, day=18)
        countries = ['us', 'gb']

        processor.process_holidays(start_date, end_date, countries)

        self.assertEqual(mock_fetch_holidays.call_count, len(countries))
        self.assertEqual(mock_save_holidays.call_count, len(countries))

        mock_fetch_holidays.assert_any_call('us', start_date, end_date)
        mock_fetch_holidays.assert_any_call('gb', start_date, end_date)

        mock_save_holidays.assert_any_call('us', mock_fetch_holidays.return_value, start_date, end_date)
        mock_save_holidays.assert_any_call('gb', mock_fetch_holidays.return_value, start_date, end_date)


if __name__ == "__main__":
    unittest.main()

