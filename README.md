# Airbnb Scraper

## Overview

This project is a web scraper for extracting Airbnb listings based on user-defined search parameters. It uses Playwright to navigate the Airbnb website, simulate user behavior, and gather relevant data, which is then saved in CSV or JSON format. Additionally, it maintains a report of search queries for future reference.

## Features

- Scrapes Airbnb listings based on query parameters such as location, check-in and check-out dates, and price range.
- Saves results in both CSV and JSON formats.
- Modular design with clear separation of concerns.

## Technologies Used

- **Python**: The main programming language.
- **Playwright**: For web scraping and automating browser interactions.
- **Pandas**: For data manipulation and saving results in various formats.
- **Argparse**: For command-line interface and argument parsing.

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/airbnb-scraper.git
cd airbnb-scraper
pip install -r requirements.txt
```

2. Acivate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

```bash
(venv) ➜  scrape_airbnb git:(main) ✗ python main.py --help
usage: main.py [-h] --query QUERY [--adults ADULTS] --checkin CHECKIN --checkout CHECKOUT [--price-min PRICE_MIN] [--price-max PRICE_MAX] [--output OUTPUT]

Airbnb scraping parameters.

options:
  -h, --help            show this help message and exit
  --query QUERY         Query location
  --adults ADULTS       Number of adults
  --checkin CHECKIN     Check-in date
  --checkout CHECKOUT   Check-out date
  --price-min PRICE_MIN
                        Minimum price
  --price-max PRICE_MAX
                        Maximum price
  --output OUTPUT       Output file (CSV or JSON)
```

The required parameters are query (location), check-in and check-out dates (in format YYYY-MM-DD).
