from lakocie_dataset.scrap import io

import os
import tempfile

FILENAME = "example.html"


def test_save_content():
    with tempfile.TemporaryDirectory() as tmpdirname:
        dir_save_path = tmpdirname
        path = os.path.join(dir_save_path, FILENAME)
        content = "Example content"
        save_path = io.save_content(content, FILENAME, dir_save_path)
        assert os.path.exists(path)
        assert save_path == path
        with open(path) as file:
            assert file.read() == content


def test_html_file_to_soup():
    with tempfile.TemporaryDirectory() as tmpdirname:
        dir_save_path = tmpdirname
        path = os.path.join(dir_save_path, FILENAME)
        content = "<html><body>Example content</body></html>"
        with open(path, "w") as file:
            file.write(content)
        soup: io.BeautifulSoup = io.html_file_to_soup(path)
        assert soup.body.text == "Example content" if soup.body else False
