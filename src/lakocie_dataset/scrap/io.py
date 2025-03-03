import os

from bs4 import BeautifulSoup


def save_content(content: str, filename: str, dir_save_path: str) -> str:
    """Save content to a file. Return path to the file. Extension **must** be specified"""
    with open(f"{dir_save_path}/{filename}", "w") as file:
        file.write(content)
    return os.path.join(dir_save_path, filename)


def html_file_to_soup(path: str) -> BeautifulSoup:
    """Return BeautifulSoup object from html file path."""
    with open(path) as file:
        return BeautifulSoup(file, "html.parser")
