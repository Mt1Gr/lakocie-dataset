import requests
from . import io, paths
from ..config import config
import time

sleep_time = config.get_sleep_time()


def get_content(url: str) -> str:
    """Fetch content from a URL."""
    response = requests.get(url)
    response.raise_for_status()
    time.sleep(sleep_time)
    return response.text


def save_html(url: str, path: paths.Path) -> paths.Path:
    """Save HTML content from a URL to a file. Return path to the file."""
    content = get_content(url)
    return io.save_content(content, path)
