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
        self._set_htmls_dir()
        self._create_structure()
        self._set_sleep_time()
        self._set_database_path()
        self._set_modes()
        self._set_dev()

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

    def _set_modes(self):
        modes = self.config.get("modes", None)
        if modes is None:
            raise ValueError("No modes defined in the config file")
        latest_info = modes.get("latest_info", {})

        if not latest_info:
            raise ValueError("No latest_info mode defined")

        self.latest_info_mode = latest_info.get("switch", False)
        self.save_to_db = latest_info.get("save_to_db", False)

        save_history_info_to_db = modes.get("save_history_info_to_db", {})
        if not save_history_info_to_db:
            raise ValueError("No save_history_info_to_db mode defined")

        self.save_history_info_to_db_mode = save_history_info_to_db.get("switch", False)
        self.save_history_info_to_db_date_choice = save_history_info_to_db.get(
            "date_choice", None
        )

        coher_database = modes.get("cohere_database", {})
        self.cohere_database_mode = coher_database.get("switch", False)

        gpt_extract_data = modes.get("gpt_extract_data", {})
        self.gpt_extract_data_mode = gpt_extract_data.get("switch", False)

    def _set_dev(self):
        dev_dict = self.config.get("dev", {})
        self.debug = dev_dict.get("debug", True)

    def get_latest_info_mode(self):
        return self.latest_info_mode

    def get_save_to_db(self):
        return self.save_to_db

    def get_save_history_info_to_db_mode(self):
        return self.save_history_info_to_db_mode

    def get_save_history_info_to_db_date_choice(self):
        return self.save_history_info_to_db_date_choice

    def get_cohere_database_mode(self):
        return self.cohere_database_mode

    def get_gpt_extract_data_mode(self):
        return self.gpt_extract_data_mode

    def get_debug(self):
        return self.debug


config = Config(Path(__file__).parent.parent.parent / "config.yaml")

if config.get_debug():
    # print(config.get_save_history_info_to_db_mode())
    # print(config.get_save_history_info_to_db_date_choice())
    print("cohere", config.get_cohere_database_mode())
    print("gpt", config.get_gpt_extract_data_mode())
