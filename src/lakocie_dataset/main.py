from sqlmodel import Session
from . import operations
from .database import sessions, models


def main():
    # operations.download_latest_html_files() # todo
    operations.save_scrapped_data_in_db()
