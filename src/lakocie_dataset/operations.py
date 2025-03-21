from datetime import datetime
from enum import Enum
from pathlib import Path
from sqlmodel import Session, select

from .scrap import downloader, scrapper, paths, io
from .scrap.stores import store_definitions
from .database import sessions, models, crud
from .openai_api import communication, output_models


def download_latest_html_files():
    print("Download latest information:")

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


def create_product_data_saver_with_register():
    # closure that handles scenerio of multiple data_scraps assign to one ean
    ean_register = set()

    def save_product_data(
        store_choice: store_definitions.StoreChoice, prod_path: Path, date: datetime
    ):
        try:
            soup = io.html_file_to_soup(prod_path)
            scrapper_ = scrapper.get_scrapper(store_choice, soup)

            store_db = crud.get_or_create_store_by_name(engine, store_choice.value.name)
            manufacturer_db = crud.get_or_create_manufacturer(
                engine, scrapper_.get_product_manufacturer()
            )

            ean = scrapper_.get_product_ean_code()
            if ean == "not found":
                return
            if ean in ean_register:
                return
            ean_register.add(ean)

            product_db = crud.get_or_create_product(
                engine, int(scrapper_.get_product_ean_code()), manufacturer_db
            )

            save_product_price_in_db(scrapper_, product_db, store_db, date)
            save_scrap_data_in_db(
                scrapper_, store_db, product_db, manufacturer_db, date
            )
        except ValueError as e:
            print(
                f"An error occurred while saving {prod_path} in db: {e}, \nskipping and proceeding to the next file"
            )
            return

    return save_product_data


def save_scrapped_data_in_db(products_download_date: str):
    print("Save scrapped data in db:")

    date: datetime
    try:
        date = datetime.strptime(products_download_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError(
            f"Invalid date format for products_download_date: {products_download_date}. Expected format: YYYY-MM-DD"
        )

    stores = list(store_definitions.StoreChoice)
    for store in stores:
        data_saver = create_product_data_saver_with_register()
        products_dir = paths.get_products_dir(store, date=products_download_date)

        for prod_path in products_dir.iterdir():
            if not prod_path.is_file():
                continue

            data_saver(store, prod_path, date)


def cohere_database():
    print("Cohere database:")

    all_valid_scrap_data = crud.read_all_valid_scrap_data(engine)
    products = crud.read_products(engine)
    followed_products = filter(lambda p: p.is_followed, products)
    products_to_unfollow = []

    # identify wieght problems
    for p in followed_products:
        scraps = [s for s in all_valid_scrap_data if s.ean == p.ean]
        if not scraps:
            products_to_unfollow.append(p)

        if all([s.weight == -1 for s in scraps]):
            products_to_unfollow.append(p)

        kf_store = crud.get_or_create_store_by_name(
            engine, store_definitions.StoreChoice.KF.value.name
        )
        kf_scraps = [s for s in scraps if s.store_id == kf_store.id]
        if "x" in kf_scraps[0].product_name.split("-")[-1]:
            products_to_unfollow.append(p)

    if products_to_unfollow != []:
        # unfollow products
        for p in products_to_unfollow:
            _ = crud.update_product(engine, p, is_followed=False)

        print("Unfollowed all products with weight problems:")
        for p in products_to_unfollow:
            print(
                f"{p.ean}: {[scrap.product_name for scrap in all_valid_scrap_data if scrap.ean == p.ean]}"
            )


class ExtractionChoice(str, Enum):
    ANALYTICAL_COMPONENTS = "składnikach analitycznych"
    DIETARY_COMPONENTS = "dodatkach dietetycznych"


def get_data_to_describe(extraction_choice: ExtractionChoice):
    unique_data = set()
    print("All products:\n\t\t\t\t", len(crud.read_products(engine)))
    with Session(engine) as session:
        followed_products = session.exec(
            select(models.Product).where(models.Product.is_followed == True)
        ).all()
        print("All followed products:\n\t\t\t\t", len(followed_products))

        count_data_to_describe = 0
        for product in followed_products:
            valid_data_scraps = []
            match extraction_choice:
                case ExtractionChoice.ANALYTICAL_COMPONENTS:
                    valid_data_scraps = [
                        ds
                        for ds in product.data_scraps
                        if ds.is_valid
                        and ds.analytical_composition != "not found"
                        and ds.analytical_components == []
                    ]
                case ExtractionChoice.DIETARY_COMPONENTS:
                    valid_data_scraps = [
                        ds
                        for ds in product.data_scraps
                        if ds.is_valid
                        and ds.dietary_supplements != "not found"
                        and ds.dietary_components == []
                    ]
            count_data_to_describe += len(valid_data_scraps)
            for ds in valid_data_scraps:
                match extraction_choice:
                    case ExtractionChoice.ANALYTICAL_COMPONENTS:
                        unique_data.add(ds.analytical_composition)
                    case ExtractionChoice.DIETARY_COMPONENTS:
                        unique_data.add(ds.dietary_supplements)

        print("Data to describe left:\n\t\t\t\t", count_data_to_describe)
        return unique_data


def describe_data_and_save_in_db(text: str, extraction_choice: ExtractionChoice):
    # find data scraps that match text
    data_scraps = []
    match extraction_choice:
        case ExtractionChoice.ANALYTICAL_COMPONENTS:
            data_scraps = crud.read_scrap_data_by_analytical_comosition(engine, text)
        case ExtractionChoice.DIETARY_COMPONENTS:
            data_scraps = crud.read_scrap_data_by_dietary_supplements(engine, text)
    if data_scraps == []:
        return

    # get gpt response
    gpt_response: (
        output_models.AnalyticalComponents | output_models.DietaryComponents | None
    ) = None
    match extraction_choice:
        case ExtractionChoice.ANALYTICAL_COMPONENTS:
            gpt_response = communication.gpt_structured_output_reuqest(
                text,
                ExtractionChoice.ANALYTICAL_COMPONENTS.value,
                output_models.AnalyticalComponents,
            )
        case ExtractionChoice.DIETARY_COMPONENTS:
            gpt_response = communication.gpt_structured_output_reuqest(
                text,
                ExtractionChoice.DIETARY_COMPONENTS.value,
                output_models.DietaryComponents,
            )
    if gpt_response is None:
        return

    # save data in db
    match extraction_choice:
        case ExtractionChoice.ANALYTICAL_COMPONENTS:
            data = gpt_response.model_dump()["components"]
            for component in data:
                if component["type"] == output_models.AnalyticalComponentType.OTHER:
                    for ds in data_scraps:
                        crud.create_analytical_component(
                            engine,
                            component["value"],
                            component["name"],
                            ds,
                        )
                else:
                    for ds in data_scraps:
                        crud.create_analytical_component(
                            engine,
                            component["value"],
                            component["type"].name.lower(),
                            ds,
                        )
        case ExtractionChoice.DIETARY_COMPONENTS:
            data = gpt_response.model_dump()["components"]
            for component in data:
                for ds in data_scraps:
                    crud.create_dietary_component(
                        engine,
                        component["value"],
                        component["unit"],
                        component["name"],
                        component["chemical_form"],
                        ds,
                    )

    print(
        f"\n\n{extraction_choice.name.lower()} described and saved in db:\n\t\t\t\t",
        len(data_scraps),
        "product names:",
    )
    for ds in data_scraps:
        print(ds.product_name)


def gpt_extract_data():
    print("Gpt extract data:")
    choices = list(ExtractionChoice)
    for choice in choices:
        unique_data_to_describe = get_data_to_describe(choice)
        if unique_data_to_describe == set():
            continue

        print("Unique data to describe:\n\t\t\t\t", len(unique_data_to_describe))
        for text in unique_data_to_describe:
            if text == "not found":
                continue
            describe_data_and_save_in_db(text, choice)

    print("All data described and saved in db")
