import uuid
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from lakocie_dataset.database.models import ScrapData, Manufacturer, Product

from lakocie_dataset.database.crud import (
    create_scrap_data,
    update_scrap_data,
    read_scrap_data,
    create_product,
    create_manufacturer,
)


def test_update_scrap_data_product_name():
    """Test updating product name in scrap data."""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    manufacturer = create_manufacturer(engine, "Test Manufacturer")
    product = create_product(engine, 1234567890, manufacturer)
    scrap_data = create_scrap_data(
        engine,
        product_name="Original Name",
        manufacturer=manufacturer,
        weight=500,
        flavour="Chicken",
        type="Dry",
        age_group="Adult",
        product=product,
        composition="Chicken, Rice",
    )

    updated = update_scrap_data(engine, scrap_data, product_name="Updated Name")

    assert updated is not None
    assert updated.product_name == "Updated Name"
    assert updated.id == scrap_data.id


def test_update_scrap_data_multiple_fields():
    """Test updating multiple fields in scrap data."""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    manufacturer = create_manufacturer(engine, "Test Manufacturer")
    product = create_product(engine, 1234567890, manufacturer)
    scrap_data = create_scrap_data(
        engine,
        product_name="Original Name",
        manufacturer=manufacturer,
        weight=500,
        flavour="Chicken",
        type="Dry",
        age_group="Adult",
        product=product,
        composition="Chicken, Rice",
    )

    updated = update_scrap_data(
        engine,
        scrap_data,
        weight=1000,
        flavour="Beef",
        composition="Beef, Rice, Vegetables",
    )

    assert updated is not None
    assert updated.weight == 1000
    assert updated.flavour == "Beef"
    assert updated.composition == "Beef, Rice, Vegetables"
    assert updated.product_name == "Original Name"  # unchanged field


def test_update_scrap_data_invalid_id():
    """Test updating scrap data with invalid ID returns None."""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    invalid_scrap_data = ScrapData(
        id=uuid.uuid4(),
        product_name="Invalid",
        weight=100,
        flavour="Unknown",
        type="Unknown",
        age_group="Unknown",
        composition="Unknown",
        ean=12345,
    )

    result = update_scrap_data(engine, invalid_scrap_data, product_name="New Name")
    assert result is None


def test_update_scrap_data_valid_flag():
    """Test updating is_valid flag in scrap data."""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    manufacturer = create_manufacturer(engine, "Test Manufacturer")
    product = create_product(engine, 1234567890, manufacturer)
    scrap_data = create_scrap_data(
        engine,
        product_name="Original Name",
        manufacturer=manufacturer,
        weight=500,
        flavour="Chicken",
        type="Dry",
        age_group="Adult",
        product=product,
        composition="Chicken, Rice",
    )

    updated = update_scrap_data(engine, scrap_data, is_valid=False)

    assert updated is not None
    assert updated.is_valid is False


def test_update_scrap_data_valid_to():
    """Test updating valid_to date in scrap data."""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    manufacturer = create_manufacturer(engine, "Test Manufacturer")
    product = create_product(engine, 1234567890, manufacturer)
    scrap_data = create_scrap_data(
        engine,
        product_name="Original Name",
        manufacturer=manufacturer,
        weight=500,
        flavour="Chicken",
        type="Dry",
        age_group="Adult",
        product=product,
        composition="Chicken, Rice",
    )

    valid_to = datetime(2023, 12, 31)
    updated = update_scrap_data(engine, scrap_data, valid_to=valid_to)

    assert updated is not None
    assert updated.valid_to == valid_to
