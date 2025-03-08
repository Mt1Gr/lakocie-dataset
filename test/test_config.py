import pytest
from pathlib import Path
from lakocie_dataset.config import Config


@pytest.fixture
def config_file(tmp_path):
    config_content = """
    paths:
        htmls_dir: "htmls"

    downloading:
        sleep_time: 1
    """
    config_path = tmp_path / "config.yaml"
    config_path.write_text(config_content)
    return config_path


def test_config_initialization(config_file):
    config = Config(config_file)
    assert config.config_file == config_file.resolve()
    assert config.project_root == config_file.parent


def test_load_yaml(config_file):
    config = Config(config_file)
    assert "paths" in config.config


def test_set_htmls_dir(config_file):
    config = Config(config_file)
    assert config.htmls_dir.is_absolute()


def test_get_htmls_dir(config_file):
    config = Config(config_file)
    htmls_dir = config.get_htmls_dir()
    assert htmls_dir.is_absolute()


def test_create_structure(config_file):
    config = Config(config_file)
    assert config.get_htmls_dir().exists()


def test_set_sleep_time(config_file):
    config = Config(config_file)
    assert config.get_sleep_time() == 1


def test_default_sleep_time(tmp_path):
    config_content = """
    paths:
        htmls: "htmls"
        data: "data"
    """
    config_path = tmp_path / "config.yaml"
    config_path.write_text(config_content)
    config = Config(config_path)
    assert config.get_sleep_time() == 2


def test_get_database_path(tmp_path):
    config_content = """
    paths:
        htmls: "htmls"
        data: "data"
        database: database.db
    """
    config_path = tmp_path / "config.yaml"
    config_path.write_text(config_content)
    config = Config(config_path)
    assert config.get_database_path() == config_path.parent / "database.db"


def test_default_database_path():
    config = Config(Path(__file__).parent.parent / "config.yaml")
    assert (
        config.get_database_path() == Path(__file__).parent.parent / "data/database.db"
    )
