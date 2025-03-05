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
        self._resolve_paths()
        self._create_structure()
        self._set_sleep_time()

    def _resolve_paths(self, paths_key: str = "paths"):
        paths = self.config.get(paths_key, {})
        for key, value in paths.items():
            abs_check = Path(value).is_absolute()
            if not abs_check:
                self.config[paths_key][key] = Path(self.project_root / value)
            else:
                self.config[paths_key][key] = Path(value)

    def _create_structure(self):
        for path in self.config["paths"].values():
            path.mkdir(parents=True, exist_ok=True)

    def get_htmls_dir(self):
        """
        Returns the path to the htmls directory
        """
        return self.config["paths"]["htmls_dir"]

    def _set_sleep_time(self):
        self.sleep_time = self.config.get("downloading", {}).get("sleep_time", 2)

    def get_sleep_time(self):
        return self.sleep_time


config = Config(Path(__file__).parent.parent.parent / "config.yaml")

# debugging
print(config.get_sleep_time())
