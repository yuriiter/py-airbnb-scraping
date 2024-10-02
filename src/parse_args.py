import argparse
from urllib.parse import urlencode
from src.config import BASE_URL
from src.file_utils import default_output_file

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Airbnb scraping parameters.')
    parser.add_argument('--query', type=str, required=True, help='Query location')
    parser.add_argument('--adults', type=str, default=1, help='Number of adults (1 by default)')
    parser.add_argument('--checkin', type=str, required=True, help='Check-in date')
    parser.add_argument('--checkout', type=str, required=True, help='Check-out date')
    parser.add_argument('--price-min', type=str, default=None, help='Minimum price')
    parser.add_argument('--price-max', type=str, default=None, help='Maximum price')
    parser.add_argument('--output', type=str, help='Output file (CSV or JSON), auto-generated CSV by default')
    parser.add_argument('--currency', type=str, help='Currency (EUR by default)', default="EUR")

    args = parser.parse_args()
    if args.output is None:
        args.output = default_output_file(args.query)

    return args

def get_encoded_params(args):
    """Create URL parameters from CLI arguments."""
    params = {
        "query": args.query,
        "checkin": args.checkin,
        "checkout": args.checkout,
        "check_in": args.checkin,
        "check_out": args.checkout,
        "adults": args.adults,
        "locale": "en",
        "currency": args.currency,
    }
    if args.price_min:
        params["price_min"] = args.price_min
    if args.price_max:
        params["price_max"] = args.price_max

    return urlencode(params)

def construct_url(args):
    """Construct the full URL for the search request."""
    encoded_params = get_encoded_params(args)
    return f"{BASE_URL}?{encoded_params}"
