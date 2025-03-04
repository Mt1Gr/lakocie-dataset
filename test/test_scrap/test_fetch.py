import os
import tempfile
from lakocie_dataset.scrap import fetch, paths

SUCCESS_URL = "https://example.com"
FAIL_URL = "https://example404"
FILENAME = "example.html"


def test_get_content():
    content = fetch.get_content(SUCCESS_URL)
    assert "Example Domain" in content


def test_save_html():
    with tempfile.TemporaryDirectory() as tmpdirname:
        save_path = paths.Path(tmpdirname) / FILENAME
        save_path = fetch.save_html(SUCCESS_URL, save_path)
        assert os.path.exists(save_path)
        with open(save_path) as file:
            content = file.read()
            assert "Example Domain" in content
