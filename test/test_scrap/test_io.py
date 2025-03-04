from lakocie_dataset.scrap import io, paths
import pytest
import tempfile

FILENAME = "example.html"


def test_save_content():
    content = "Hello, World!"
    with tempfile.TemporaryDirectory() as tmpdir:
        path = paths.Path(tmpdir) / FILENAME
        saved_path = io.save_content(content, path)
        assert saved_path == path
        assert saved_path.exists()
        with open(saved_path) as file:
            assert file.read() == content


def test_save_content_raises():
    not_existing_parent = paths.Path("not_existing")
    with tempfile.TemporaryDirectory() as tmpdir:
        already_existing_file = paths.Path(tmpdir) / FILENAME
        already_existing_file.touch()

        with pytest.raises(FileNotFoundError):
            io.save_content("content", not_existing_parent / FILENAME)

        with pytest.raises(FileExistsError):
            io.save_content("content", already_existing_file)


def test_html_file_to_soup():
    content = "<html><body><h1>Hello, World!</h1></body></html>"
    with tempfile.TemporaryDirectory() as tmpdir:
        path = paths.Path(tmpdir) / FILENAME
        with open(path, "w") as file:
            file.write(content)
        soup = io.html_file_to_soup(path)
        h1_tag = soup.find("h1") if soup else None
        assert h1_tag
        assert h1_tag.text == "Hello, World!"


def test_html_file_to_soup_raises():
    with tempfile.TemporaryDirectory() as tmpdir:
        not_existing_file = paths.Path(tmpdir) / "not_existing.html"
        with pytest.raises(FileNotFoundError):
            io.html_file_to_soup(not_existing_file)

        not_html_file = paths.Path(tmpdir) / "not_html.txt"
        not_html_file.touch()
        with pytest.raises(ValueError):
            io.html_file_to_soup(not_html_file)
