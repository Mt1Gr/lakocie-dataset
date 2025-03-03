import os


def save_content(content: str, filename: str, dir_save_path: str) -> str:
    """Save content to a file. Return path to the file."""
    with open(f"{dir_save_path}/{filename}", "w") as file:
        file.write(content)
    return os.path.join(dir_save_path, filename)
