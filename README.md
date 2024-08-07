# Holiday API Collector

## Overview

The **Holiday API Collector** is a Python project that fetches holiday data for specified countries from the Calendarific API. It allows you to collect holiday information between given start and end dates, and saves this data in JSON format, divided by country.

## Features

- Fetch holiday data from the Calendarific API.
- Supports multiple countries.
- Saves holiday data in JSON format to files.
- Includes logging for monitoring script execution.
- Comes with unit tests for ensuring functionality.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/holiday-api-collector.git
   cd holiday-api-collector

## Set Up Environment

1. **Create a `.env` File**

   Create a file named `.env` in the project root directory with the following content:

   ```plaintext
   CALENDARIFIC_API_KEY=your_api_key_here

## Install Dependencies

1. **Create and Activate a Virtual Environment**

   First, create a virtual environment in the project directory:

   ```bash
   python -m venv venv
   ```

   After creating the virtual environment, activate it:
- on Windows
   ```
   venv\Scripts\activate
   ```
- on Linux
   ```
   source venv/bin/activate
   ```

## Install Required Packages
   With the virtual environment activated, install the necessary dependencies using the requirements.txt file
   ```bash
   pip install -r requirements.txt
   ```
## Verify Installed Packages
   To ensure that the required packages have been installed correctly, you can list the installed packages:
   ```bash
   pip list
   ```

## Usage
   To run the script and fetch holidays for specified countries, use the following Python command:
   ```
   python main.py

   ```
   Modify the main.py script to specify your desired start_date, end_date, and countries_list.
   

## Running Tests
   To run all tests in the project, use:
   ```
   python -m unittest discover -s tests
   ```

## License
   This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
   

## Contact
   For any questions or feedback, please reach out to romanuik7meri.ua@gmail.com.