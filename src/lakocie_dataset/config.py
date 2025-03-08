import yaml
from pathlib import Path


class Config:
    """Configuration class for managing project paths and settings.
    This class handles loading configuration from a YAML file, resolving paths,
    and creating necessary directory structures.
    Args:
        config_file (Path): Path to the YAML configuration file.
    Attributes:
        config_file (Path): Resolved path to the configuration file
        project_root (Path): Parent directory of the config file
        config (dict): Loaded configuration from YAML file
    Methods:
        _load_yaml(): Loads configuration from YAML file and sets up paths
        _resolve_paths(paths_key='paths'): Resolves relative paths to absolute paths
        _create_structure(): Creates directories defined in the config paths
        get_htmls_dir(): Returns path to the htmls directory
    """

    def __init__(self, config_file: Path):
        self.config_file = Path(config_file).resolve()
        self.project_root = self.config_file.parent
        self._load_yaml()

    def _load_yaml(self):
        with open(self.config_file, "r") as file:
            self.config = yaml.safe_load(file)
        self._set_htmls_dir()
        self._create_structure()
        self._set_sleep_time()
        self._set_database_path()

    def _set_htmls_dir(self, paths_key: str = "paths"):
        htmls_dir = Path(self.config.get(paths_key, {}).get("htmls_dir", "data/htmls"))
        if not htmls_dir.is_absolute():
            htmls_dir = self.project_root / htmls_dir
        self.htmls_dir = htmls_dir

    def _create_structure(self):
        self.htmls_dir.mkdir(parents=True, exist_ok=True)

    def get_htmls_dir(self):
        """
        Returns the path to the htmls directory
        """
        return self.htmls_dir

    def _set_sleep_time(self):
        self.sleep_time = self.config.get("downloading", {}).get("sleep_time", 2)

    def get_sleep_time(self):
        return self.sleep_time

    def _set_database_path(self):
        db_path = Path(self.config.get("paths", {}).get("database", "data/database.db"))
        if not db_path.is_absolute():
            db_path = self.project_root / db_path
        self.database_path = db_path

    def get_database_path(self):
        return self.database_path


config = Config(Path(__file__).parent.parent.parent / "config.yaml")
