from . import operations
from .scrap.paths import get_today_date_string
from .config import config


def main():
    if config.get_latest_info_mode():
        operations.download_latest_html_files()
        if config.get_save_to_db():
            operations.save_scrapped_data_in_db(get_today_date_string())

    if config.get_save_history_info_to_db_mode():
        date = config.get_save_history_info_to_db_date_choice()
        if date:
            operations.save_scrapped_data_in_db(date)

    if config.get_cohere_database_mode():
        operations.cohere_database()

    if config.get_gpt_extract_data_mode():
        operations.gpt_extract_data()
