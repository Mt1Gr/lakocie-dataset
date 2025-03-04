import os
from . import paths
from bs4 import BeautifulSoup


def save_content(content: str, path: paths.Path) -> paths.Path:
    """Save content to a file. Return path to the saved file."""
    if not isinstance(path, paths.Path):
        raise TypeError(f"Expected Path object, got {type(path)}")
    elif not path.parent.exists():
        raise FileNotFoundError(f"Directory {path.parent} not found.")
    elif path.exists():
        raise FileExistsError(f"File {path} already exists.")

    with open(path, "w") as file:
        file.write(content)
    return path


def html_file_to_soup(path: paths.Path) -> BeautifulSoup:
    """Return BeautifulSoup object from html file path."""
    if not isinstance(path, paths.Path):
        raise TypeError(f"Expected Path object, got {type(path)}")
    elif not os.path.exists(path):
        raise FileNotFoundError(f"File {path} not found.")
    elif not path.name.endswith(".html"):
        raise ValueError(f"File {path} is not an html file.")

    with open(path) as file:
        return BeautifulSoup(file, "html.parser")
