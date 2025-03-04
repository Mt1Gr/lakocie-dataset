import yaml
from pathlib import Path


class Config:
    def __init__(self, config_file: Path):
        self.config_file = Path(config_file).resolve()
        self.project_root = self.config_file.parent
        self._load_yaml()

    def _load_yaml(self):
        with open(self.config_file, "r") as file:
            self.config = yaml.safe_load(file)
        self._resolve_paths()
        self._create_structure()

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

    def get_htmls(self):
        return self.config["paths"]["htmls"]


config = Config(Path(__file__).parent.parent.parent / "config.yaml")
print(config.config)
