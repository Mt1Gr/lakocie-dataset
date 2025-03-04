import pytest
from pathlib import Path
from lakocie_dataset.config import Config


def test_config_initialization(tmp_path):
    # Create a temporary config file
    config_content = """
    paths:
        htmls: htmls
        data: data
    """
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)

    # Initialize config
    config = Config(config_file)

    # Test basic attributes
    assert config.config_file == config_file.resolve()
    assert config.project_root == tmp_path


def test_path_resolution(tmp_path):
    config_content = """
    paths:
        htmls: htmls
        data: data
    """
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)

    config = Config(config_file)

    # Test paths were resolved
    assert config.config["paths"]["htmls"] == tmp_path / "htmls"
    assert config.config["paths"]["data"] == tmp_path / "data"


def test_directory_creation(tmp_path):
    config_content = """
    paths:
        dir1: test_dir1
        dir2: nested/test_dir2
    """
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)

    config = Config(config_file)

    # Test directories were created
    assert (tmp_path / "test_dir1").exists()
    assert (tmp_path / "nested/test_dir2").exists()


def test_get_htmls(tmp_path):
    config_content = """
    paths:
        htmls: html_directory
    """
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)

    config = Config(config_file)

    assert config.get_htmls_dir() == tmp_path / "html_directory"


def test_invalid_config_file():
    with pytest.raises(FileNotFoundError):
        Config(Path("nonexistent.yaml"))
