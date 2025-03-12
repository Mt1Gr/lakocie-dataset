from datetime import datetime
from pathlib import Path
from .scrap import downloader, scrapper, paths, io
from .scrap.stores import store_definitions
from .database import sessions, models, crud


def download_latest_html_files():
    downloader.download_collection_files()
    downloader.download_product_files()


engine = sessions.create_db_and_tables()


def save_scrap_data_in_db(
    scrapper_: scrapper.Scrapper,
    store: models.Store,
    product: models.Product,
    manufacturer: models.Manufacturer,
    date: datetime = datetime.now(),
):
    valid_scrap_data = crud.read_valid_scrap_data_by_product_and_store(
        engine, product, store
    )

    scrap_compostion = scrapper_.get_product_composition()
    scrap_analytical_composition = scrapper_.get_product_analytical_composition()
    scrap_dietary_supplements = scrapper_.get_product_dietary_supplements()

    if valid_scrap_data:
        conditions = [
            valid_scrap_data.composition == scrap_compostion,
            valid_scrap_data.analytical_composition == scrap_analytical_composition,
            valid_scrap_data.dietary_supplements == scrap_dietary_supplements,
        ]
        if all(conditions):
            if valid_scrap_data.valid_from > date:
                _ = crud.update_scrap_data(
                    engine, valid_scrap_data, is_valid=True, valid_from=date
                )
            return
        else:
            _ = crud.update_scrap_data(
                engine, valid_scrap_data, is_valid=False, valid_to=datetime.now()
            )
    scrap_data_dict = {
        "product_name": scrapper_.get_product_name(),
        "manyfacturer": manufacturer,
        "weight": scrapper_.get_product_weight(),
        "flavour": scrapper_.get_product_flavour(),
        "type": scrapper_.get_product_type(),
        "age_group": scrapper_.get_product_age_group(),
        "product": product,
        "composition": scrap_compostion,
        "analytical_composition": scrap_analytical_composition,
        "dietary_supplements": scrap_dietary_supplements,
        "store": store,
        "date": date,
    }

    _ = crud.create_scrap_data(engine, **scrap_data_dict)


def save_product_price_in_db(
    scrapper_: scrapper.Scrapper,
    product_db: models.Product,
    store_db: models.Store,
    date: datetime,
):
    same_price_in_db = crud.read_price_by_product_store_and_date(
        engine, product_db, store_db, date
    )
    if same_price_in_db:
        return
    price = scrapper_.get_product_price()
    if price == "not found":
        return
    _ = crud.create_price(engine, price, product_db, store_db, date)


def save_product_data_in_db(store_choice, prod_path: Path, date: datetime):
    try:
        soup = io.html_file_to_soup(prod_path)
        scrapper_ = scrapper.get_scrapper(store_choice, soup)

        store_db = crud.get_or_create_store(engine, store_choice.value.name)
        manufacturer_db = crud.get_or_create_manufacturer(
            engine, scrapper_.get_product_manufacturer()
        )

        ean = scrapper_.get_product_ean_code()
        if ean == "not found":
            return
        product_db = crud.get_or_create_product(
            engine, int(scrapper_.get_product_ean_code()), manufacturer_db
        )

        save_product_price_in_db(scrapper_, product_db, store_db, date)
        save_scrap_data_in_db(scrapper_, store_db, product_db, manufacturer_db, date)
    except ValueError as e:
        print(f"An error occurred while saving {prod_path} in db: {e}")
        return


# def


def save_scrapped_data_in_db(products_download_date: str):
    date: datetime
    try:
        date = datetime.strptime(products_download_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError(
            f"Invalid date format for products_download_date: {products_download_date}. Expected format: YYYY-MM-DD"
        )

    stores = list(store_definitions.StoreChoice)
    for store in stores:
        products_dir = paths.get_products_dir(store, date=products_download_date)

        for prod_path in products_dir.iterdir():
            if not prod_path.is_file():
                continue

            save_product_data_in_db(store, prod_path, date)
