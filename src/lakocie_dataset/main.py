from .scrap import downloader
from .database import sessions

mode = ["init_db"]


def main():
    if "download_files" in mode:
        downloader.download_collection_files()
        downloader.download_product_files()

    if "init_db" in mode:
        engine = sessions.create_db_and_tables()
