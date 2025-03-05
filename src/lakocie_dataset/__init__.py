from .scrap import downloader


# debugging
def main():
    downloader.download_collection_files()
    downloader.download_product_files()


if __name__ == "__main__":
    main()
