import time
from . import io, fetch, paths, permissions, scrapper
from .stores import store_definitions, string_utils
from ..config import config


def download_collection_files():
    """Download all files that contain products links"""
    sleep_time = config.get_sleep_time()
    stores = list(store_definitions.StoreChoice)
    for store in stores:
        try:
            if not permissions.webscrapping_allowed(store.value.base_url):
                print(f"Web scrapping not allowed for {store}")
                continue
            collection_dir = paths.create_collections_dir(store)
            count = 1
            save_path = collection_dir / f"collection_{count}.html"
            if save_path.exists():
                print(f"File {save_path} already exists")
            else:
                fetch.save_html(store.value.scrap_start_url, save_path)
                print(f"downloaded file:\t{save_path}")
            soup = io.html_file_to_soup(save_path)
            sc = scrapper.get_scrapper(store, soup)
            next_page_link = sc.get_next_page_link()
            while next_page_link:
                count += 1
                save_path = collection_dir / f"collection_{count}.html"
                if save_path.exists():
                    print(f"File {save_path} already exists")
                else:
                    time.sleep(sleep_time)
                    fetch.save_html(next_page_link, save_path)
                    print(f"downloaded file:\t{save_path}")
                soup = io.html_file_to_soup(save_path)
                sc.change_soup(soup)
                next_page_link = sc.get_next_page_link()
        except Exception as e:
            print(f"A problem occurred while downloading {store} collection files: {e}")
            continue


def download_product_files():
    """Download all files that contain product information"""
    sleep_time = config.get_sleep_time()
    stores = list(store_definitions.StoreChoice)
    for store in stores:
        if not permissions.webscrapping_allowed(store.value.base_url):
            print(f"Web scrapping not allowed for {store}")
            continue
        collections_dir = paths.get_latest_collections_dir(store)
        products_dir = paths.create_products_dir(store)
        for coll in collections_dir.iterdir():
            try:
                soup = io.html_file_to_soup(coll)
                sc = scrapper.get_scrapper(store, soup)
                product_links = sc.get_product_links()
                for link in product_links:
                    save_path = (
                        products_dir
                        / f"{string_utils.product_name_from_url(link, store)}.html"
                    )
                    if save_path.exists():
                        print(f"File {save_path} already exists")
                    else:
                        time.sleep(sleep_time)
                        fetch.save_html(link, save_path)
                        print(f"downloaded file:\t{save_path}")
            except Exception as e:
                print(
                    f"A problem occurred while downloading {store} product files: {e}"
                )
                continue
