from pathlib import Path
import os
from datetime import datetime
from .stores import StoreChoice
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
    return products_dir


def get_collections_dir(
    store: StoreChoice, date: str = get_today_date_string(), config=config
):
    """
    Returns the path to the collections directory for a given store and date
    """
    date_dir = config.get_htmls_dir() / store.value.name / date
    collections_dir = date_dir / "collections"
    return collections_dir
