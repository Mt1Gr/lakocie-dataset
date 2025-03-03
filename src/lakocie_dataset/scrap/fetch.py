import requests
from . import io


def get_content(url: str) -> str:
    """Fetch content from a URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def save_html(url: str, dir_save_path: str, filename: str) -> str:
    """Save HTML content from a URL to a file. Return path to the file."""
    content = get_content(url)
    return io.save_content(content, filename, dir_save_path)
