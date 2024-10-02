from src.config import USE_PROXY

def get_random_proxy():
    """Return a random proxy if USE_PROXY is enabled."""
    if not USE_PROXY:
        return None
    # return swift.proxy()  # Implement your proxy logic

def create_new_context_with_state(browser, new_proxy):
    """Create a new browser context with an optional proxy."""
    return browser.new_context(proxy={'server': new_proxy} if new_proxy else None)
