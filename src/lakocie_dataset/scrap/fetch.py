import requests
from . import io, paths


def get_content(url: str) -> str:
    """Fetch content from a URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def save_html(url: str, path: paths.Path) -> paths.Path:
    """Save HTML content from a URL to a file. Return path to the file."""
    content = get_content(url)
    return io.save_content(content, path)
