import traceback
import random
import time
from playwright.sync_api import sync_playwright

from src.config import PAGES_PER_PROXY, USE_PROXY, ROTATE_PROXY
from src.file_utils import create_if_not_exists
from src.parse_args import get_encoded_params, construct_url, parse_args
from src.proxy  import get_random_proxy, create_new_context_with_state
from src.reporting import save_search_results, append_to_reports_csv
from src.retrieve_data import handle_response


def mimic_human_behaviour(page, total_time):
    """Simulate human-like scrolling behavior on the page."""
    num_actions = random.randint(3, 6)
    action_time = total_time / num_actions

    for _ in range(num_actions):
        scroll_distance = random.randint(100, 500)
        scroll_direction = random.choice(['down', 'up'])
        page.evaluate(f'window.scrollBy(0, {scroll_distance * (1 if scroll_direction == "down" else -1)});')
        time.sleep(action_time * random.uniform(0.5, 1.5))

def search_current(page):
    """Perform the search on the Airbnb page."""
    page.wait_for_selector('button[aria-describedby="searchInputDescriptionId"]')
    page.click('button[aria-describedby="searchInputDescriptionId"]')
    page.wait_for_selector('button[data-testid="explore-footer-primary-btn"]')
    page.click('button[data-testid="explore-footer-primary-btn"]')


def scrape():
    """Main scraping function."""
    create_if_not_exists('generated/')
    args = parse_args()
    print('Starting scraping AirBnb...')
    output_file = args.output
    url = construct_url(args)
    listings = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        proxy = get_random_proxy()
        context = browser.new_context(viewport={'width': 450, 'height': 800}, proxy={'server': proxy} if proxy else None)
        page = context.new_page()

        page.goto(url)
        search_current(page)

        idx = 0
        while True:
            try:
                idx += 1
                with page.expect_response(lambda response: "operationName=StaysSearch" in response.url) as response_event:
                    handle_response(response_event.value, get_encoded_params(args), listings)

                if idx % PAGES_PER_PROXY == 0 and USE_PROXY and ROTATE_PROXY:
                    print('Changing proxy server')
                    current_url = page.url
                    context = create_new_context_with_state(browser, None)
                    page = context.new_page()
                    page.goto(current_url)
                    page.wait_for_selector('a[aria-label="Next page"]')

                next_button = page.query_selector('a[aria-label="Next page"]')
                if not next_button:
                    print("Finished")
                    break

                next_button.click()
                print("Next page")

            except Exception as e:
                traceback.print_exception(e)
                break

        browser.close()

        save_search_results(listings, output_file)
        append_to_reports_csv(args)

if __name__ == "__main__":
    scrape()
