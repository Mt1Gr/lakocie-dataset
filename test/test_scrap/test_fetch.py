import os
import tempfile
from lakocie_dataset.scrap import fetch

SUCCESS_URL = "https://example.com"
FAIL_URL = "https://example404"
FILENAME = "example.html"


def test_get_content():
    content = fetch.get_content(SUCCESS_URL)
    assert "Example Domain" in content


def test_save_html():
    with tempfile.TemporaryDirectory() as tmpdirname:
        save_path = fetch.save_html(SUCCESS_URL, tmpdirname, FILENAME)
        assert os.path.exists(save_path)
        with open(save_path) as file:
            content = file.read()
            assert "Example Domain" in content
