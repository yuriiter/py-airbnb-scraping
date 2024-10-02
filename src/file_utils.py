import time
from datetime import datetime
import os

def create_if_not_exists(path):
    """
    Create directories recursively if they don't exist.
    
    If the path ends with '/', it treats the path as a directory.
    If the path does not end with '/', it treats the path as a file
    and ensures that the directory exists.
    """
    if path.endswith('/'):
        os.makedirs(path, exist_ok=True)
    else:
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
            open(path, 'a').close()

def default_output_file(query):
    """Generate a default output filename based on the query and current date."""
    now = datetime.now()
    num_of_milliseconds = int(time.time() * 1000) % 1000
    return f"generated/{query}_{now.strftime('%Y%m%d')}_{num_of_milliseconds}.csv"
