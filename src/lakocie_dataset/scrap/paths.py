from pathlib import Path
from datetime import datetime
from .stores.store_definitions import StoreChoice
from ..config import config


def get_today_date_string() -> str:
    """
    Returns the current date in YYYY-MM-DD format
    """
    return datetime.now().strftime("%Y-%m-%d")


def create_date_dir(
    store: StoreChoice, date: str = get_today_date_string(), config=config
) -> Path:
    """
    Creates a directory for the current date in the store's htmls directory
    """
    store_dir = config.get_htmls_dir() / store.value.name
    date_dir = store_dir / date
    date_dir.mkdir(parents=True, exist_ok=True)
    return date_dir


def create_products_dir(
    store: StoreChoice, date: str = get_today_date_string(), config=config
) -> Path:
    """
    Creates a directory for products in the store's htmls directory
    """
    date_dir = create_date_dir(store, date=date, config=config)
    products_dir = date_dir / "products"
    products_dir.mkdir(parents=True, exist_ok=True)
    return products_dir


def create_collections_dir(
    store: StoreChoice, date: str = get_today_date_string(), config=config
) -> Path:
    """
    Creates a directory for collections in the store's htmls directory
    """
    date_dir = create_date_dir(store, date=date, config=config)
    collections_dir = date_dir / "collections"
    collections_dir.mkdir(parents=True, exist_ok=True)
    return collections_dir


def get_products_dir(
    store: StoreChoice, date: str = get_today_date_string(), config=config
):
    """
    Returns the path to the products directory for a given store and date
    """
    date_dir = config.get_htmls_dir() / store.value.name / date
    products_dir = date_dir / "products"
    if not products_dir.exists():
        raise FileNotFoundError(f"Products directory not found for {store} on {date}")
    return products_dir


def get_collections_dir(
    store: StoreChoice, date: str = get_today_date_string(), config=config
):
    """
    Returns the path to the collections directory for a given store and date
    """
    date_dir = config.get_htmls_dir() / store.value.name / date
    collections_dir = date_dir / "collections"
    if not collections_dir.exists():
        raise FileNotFoundError(
            f"Collections directory not found for {store} on {date}"
        )
    return collections_dir


def get_latest_products_dir(store: StoreChoice, config=config) -> Path:
    """
    Returns the path to the latest products directory for a given store
    """
    store_dir = config.get_htmls_dir() / store.value.name
    date_dirs = sorted(store_dir.glob("*"), reverse=True)
    for date_dir in date_dirs:
        products_dir = date_dir / "products"
        if products_dir.exists():
            return products_dir
    raise FileNotFoundError(f"Products directory not found for {store}")


def get_latest_collections_dir(store: StoreChoice, config=config) -> Path:
    """
    Returns the path to the latest collections directory for a given store
    """
    store_dir = config.get_htmls_dir() / store.value.name
    date_dirs = sorted(store_dir.glob("*"), reverse=True)
    for date_dir in date_dirs:
        collections_dir = date_dir / "collections"
        if collections_dir.exists():
            return collections_dir
    raise FileNotFoundError(f"Collections directory not found for {store}")
