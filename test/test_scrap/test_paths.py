from pathlib import Path
from lakocie_dataset.scrap import paths
from datetime import datetime
from lakocie_dataset.scrap.stores.store_definitions import StoreChoice
from lakocie_dataset.config import Config
import pytest

test_config = None
TEST_CONFIG_PATH = Path(__file__).parent.parent / "test-config.yaml"


def setup_module(module):
    global test_config, TEST_CONFIG_PATH
    if not TEST_CONFIG_PATH.exists():
        TEST_CONFIG_PATH.touch()
        with open(TEST_CONFIG_PATH, "w") as file:
            file.write(
                """
paths:
  htmls_dir: test-data/htmls
"""
            )
    test_config = Config(TEST_CONFIG_PATH)


def test_get_today_date_string():
    date_str = paths.get_today_date_string()
    # Check if returned string matches YYYY-MM-DD format
    assert len(date_str) == 10
    assert datetime.strptime(date_str, "%Y-%m-%d")
    # Check if returned date is today
    assert date_str == datetime.now().strftime("%Y-%m-%d")


def test_create_date_dir():
    global test_config
    stores = list(StoreChoice)
    for store in stores:
        date_dir = paths.create_date_dir(store, config=test_config)  # type: ignore
        assert date_dir.exists()


def test_create_products_dir():
    global test_config
    stores = list(StoreChoice)
    for store in stores:
        match store:
            case StoreChoice.KF:
                products_dir = paths.create_products_dir(store, config=test_config)  # type: ignore
                assert products_dir.exists()
            case _:
                raise NotImplementedError(f"Products not supported for store {store}")


def test_create_collections_dir():
    global test_config
    stores = list(StoreChoice)
    for store in stores:
        match store:
            case StoreChoice.KF:
                collections_dir = paths.create_collections_dir(
                    store,
                    config=test_config,  # type: ignore
                )
                assert collections_dir.exists()
            case _:
                raise NotImplementedError(
                    f"Collections not supported for store {store}"
                )


def test_get_products_dir():
    global test_config
    stores = list(StoreChoice)
    for store in stores:
        match store:
            case StoreChoice.KF:
                products_dir = paths.get_products_dir(store, config=test_config)  # type: ignore
                assert products_dir.exists()
            case _:
                raise NotImplementedError(f"Products not supported for store {store}")

    for store in stores:
        match store:
            case StoreChoice.KF:
                with pytest.raises(FileNotFoundError):
                    products_dir = paths.get_products_dir(  # type: ignore
                        store,
                        date="2020-20-20",
                        config=test_config,  # type: ignore
                    )
                    assert products_dir.exists() is False
            case _:
                raise NotImplementedError(f"Products not supported for store {store}")

    for store in stores:
        paths.create_products_dir(store, date="2021-01-01", config=test_config)  # type: ignore

    for store in stores:
        match store:
            case StoreChoice.KF:
                products_dir = paths.get_products_dir(  # type: ignore
                    store,
                    date="2021-01-01",
                    config=test_config,  # type: ignore
                )
                assert products_dir.exists()
            case _:
                raise NotImplementedError(f"Products not supported for store {store}")


def test_get_collections_dir():
    global test_config
    stores = list(StoreChoice)
    for store in stores:
        match store:
            case StoreChoice.KF:
                collections_dir = paths.get_collections_dir(store, config=test_config)  # type: ignore
                assert collections_dir.exists()
            case _:
                raise NotImplementedError(
                    f"Collections not supported for store {store}"
                )

    for store in stores:
        match store:
            case StoreChoice.KF:
                with pytest.raises(FileNotFoundError):
                    collections_dir = paths.get_collections_dir(  # type: ignore
                        store,
                        date="2020-20-20",
                        config=test_config,  # type: ignore
                    )
                    assert collections_dir.exists() is False
            case _:
                raise NotImplementedError(
                    f"Collections not supported for store {store}"
                )

    for store in stores:
        paths.create_collections_dir(store, date="2021-01-01", config=test_config)  # type: ignore

    for store in stores:
        match store:
            case StoreChoice.KF:
                collections_dir = paths.get_collections_dir(  # type: ignore
                    store,
                    date="2021-01-01",
                    config=test_config,  # type: ignore
                )
                assert collections_dir.exists()
            case _:
                raise NotImplementedError(
                    f"Collections not supported for store {store}"
                )


def test_get_latest_products_dir():
    global test_config
    stores = list(StoreChoice)
    for store in stores:
        match store:
            case StoreChoice.KF:
                today_prod_dir = paths.create_products_dir(store, config=test_config)  # type: ignore

                products_dir = paths.get_latest_products_dir(store, config=test_config)  # type: ignore
                assert products_dir.exists()
                assert products_dir == today_prod_dir
            case _:
                raise NotImplementedError(f"Products not supported for store {store}")


def test_get_latest_collections_dir():
    global test_config
    stores = list(StoreChoice)
    for store in stores:
        match store:
            case StoreChoice.KF:
                today_coll_dir = paths.create_collections_dir(store, config=test_config)  # type: ignore

                collections_dir = paths.get_latest_collections_dir(
                    store,
                    config=test_config,  # type: ignore
                )
                assert collections_dir.exists()
                assert collections_dir == today_coll_dir
            case _:
                raise NotImplementedError(
                    f"Collections not supported for store {store}"
                )
