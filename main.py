import os
import requests
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

# Load API Key from .env file
load_dotenv()
API_KEY = os.getenv('CALENDARIFIC_API_KEY')

BASE_URL = "https://calendarific.com/api/v2/holidays"


class HolidayCollector:
    """
        A class responsible for fetching holiday data from the Calendarific API.

        Attributes:
            api_key (str): The API key for authenticating requests to the Calendarific API.
            base_url (str): The base URL of the Calendarific API.
    """

    def __init__(self, api_key: str):
        """
        Initializes the HolidayCollector with the provided API key.

        Args:
            api_key (str): The API key used to authenticate with the Calendarific API.
        """
        self.api_key = api_key
        self.base_url = BASE_URL

    def fetch_holidays(self, country: str, start_date: datetime, end_date: datetime) -> list:
        """
        Fetches holidays for a specific country between the given start and end dates.

        Args:
            country (str): The country code for which to fetch holidays.
            start_date (datetime): The start date of the period to fetch holidays for.
            end_date (datetime): The end date of the period to fetch holidays for.

        Returns:
            list: A list of dictionaries, each representing a holiday.
        """
        params = {
            'country': country,
            'year': start_date.year,
            'start': start_date.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d')
        }

        response = requests.get(
            self.base_url,
            auth=HTTPBasicAuth('apikey', self.api_key),
            params=params
        )

        response.raise_for_status()
        data = response.json()
        logging.info(f"Fetched data for {country}: {data}")

        holidays = data.get('response', {}).get('holidays', [])
        logging.info(f"Holidays for {country}: {holidays}")

        return holidays


class HolidaySaver:
    """
    A class responsible for saving holiday data to files.

    Attributes:
        output_dir (str): The directory where holiday files will be saved.
    """
    def __init__(self, output_dir: str = "output_files"):
        """
        Initializes the HolidaySaver with the provided output directory.

        Args:
            output_dir (str): The directory where files will be saved. Default is "output_files".
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save_holidays(self, country: str, holidays: list, start_date: datetime, end_date: datetime) -> None:
        """
        Saves holiday data to a file, with one file per country.

        Args:
            country (str): The country code for which holidays are being saved.
            holidays (list): A list of holiday data to be saved.
            start_date (datetime): The start date of the period for the filename.
            end_date (datetime): The end date of the period for the filename.

        Returns:
            None
        """
        start_str = start_date.strftime('%d-%m-%Y')
        end_str = end_date.strftime('%d-%m-%Y')
        file_name = f"{country}_{start_str}_{end_str}.txt"
        file_path = os.path.join(self.output_dir, file_name)

        with open(file_path, 'w') as f:
            for holiday in holidays:
                json_string = json.dumps(holiday)
                f.write(json_string + "\n")

        logging.info(f"Holidays saved to {file_path}")


class HolidayProcessor:
    """
    A class that orchestrates the fetching and saving of holiday data.

    Attributes:
        collector (HolidayCollector): An instance of the HolidayCollector class.
        saver (HolidaySaver): An instance of the HolidaySaver class.
    """
    def __init__(self, api_key: str):
        """
        Initializes the HolidayProcessor with the provided API key.

        Args:
            api_key (str): The API key used for authenticating requests to the Calendarific API.
        """
        self.collector = HolidayCollector(api_key)
        self.saver = HolidaySaver()

    def process_holidays(self, start_date: datetime, end_date: datetime, countries_list: list) -> None:
        """
        Processes holidays for multiple countries by fetching and saving them.

        Args:
            start_date (datetime): The start date of the period for which holidays should be processed.
            end_date (datetime): The end date of the period for which holidays should be processed.
            countries_list (list): A list of country codes for which to process holidays.

        Returns:
            None
        """
        for country in countries_list:
            holidays = self.collector.fetch_holidays(country, start_date, end_date)
            self.saver.save_holidays(country, holidays, start_date, end_date)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    countries = ['ua', 'us', 'gb']
    start_time = datetime(year=1992, month=7, day=7)
    end_time = datetime(year=1992, month=9, day=18)

    processor = HolidayProcessor(API_KEY)
    processor.process_holidays(start_time, end_time, countries)

