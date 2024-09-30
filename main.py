from playwright.sync_api import sync_playwright
import argparse
from urllib.parse import urlencode

def parse_args():
    parser = argparse.ArgumentParser(description='Airbnb scraping parameters.')
    parser.add_argument('--query', type=str, required=True, help='Query location')
    parser.add_argument('--adults', type=str, required=True, help='Number of adults')
    parser.add_argument('--checkin', type=str, required=True, help='Check-in date')
    parser.add_argument('--checkout', type=str, required=True, help='Check-out date')
    parser.add_argument('--price_min', type=str, help='Minimum price', default=None)
    parser.add_argument('--price_max', type=str, help='Maximum price', default=None)

    return parser.parse_args()

base_url = "https://airbnb.com/s/Germany/homes"

def construct_url(args):
    params = {
        "query": args.query,
        "checkin": args.checkin,
        "checkout": args.checkout,
        "adults": args.adults,
        "locale": "en",
        "currency": "EUR",
    }

    if args.price_min:
        params["price_min"] = args.price_min
    if args.price_max:
        params["price_max"] = args.price_max

    return f"{base_url}?{urlencode(params)}"

def scrape():
    args = parse_args()
    url = construct_url(args)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        responses = []

        def handle_response(response):
            if "operationName=StaysMapS2Search" in response.url:
                print("Filtered response from:", response.url)
                json_response = response.json()
                print("Response data:", json_response)
                responses.append(json_response)

        page.goto(url)

        while True:
            try:
                with page.expect_response(lambda response: "operationName=StaysMapS2Search" in response.url) as response_event:
                    response_event.value
                    handle_response(response_event.value)

                next_button = page.query_selector('a[aria-label="Next"]')
                if not next_button:
                    print("No 'Next' button found. Exiting.")
                    break

                next_href = next_button.get_attribute('href')
                print(f"Next URL: {next_href}")

                page.goto(f"https://airbnb.com{next_href}")

            except Exception as e:
                print(f"Error during pagination: {e}")
                break

        browser.close()

# Entry point
if __name__ == "__main__":
    scrape()
