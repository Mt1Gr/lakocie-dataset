from datetime import datetime
from typing import Optional, Sequence, List
import uuid
from sqlmodel import Session, select
from sqlalchemy import Engine
from .models import (
    DietaryComponent,
    AnalyticalComponent,
    Price,
    Product,
    Manufacturer,
    ScrapData,
    Store,
)


def create_product(
    engine: Engine, ean: int, manufacturer: Optional[Manufacturer] = None
) -> Product:
    """Create a new product in the database.

    Args:
        engine: SQLAlchemy engine
        ean: European Article Number
        manufacturer: Optional manufacturer for the product

    Returns:
        The created Product instance
    """
    with Session(engine) as session:
        product = Product(ean=ean)
        if manufacturer:
            product.manufacturer = manufacturer
        session.add(product)
        session.commit()
        session.refresh(product)
        return product


def update_product(
    engine: Engine,
    product: Product,
    manufacturer: Optional[Manufacturer] = None,
    is_followed: Optional[bool] = None,
) -> Optional[Product]:
    """Update an existing product.

    Args:
        engine: SQLAlchemy engine
        product: Product to update
        manufacturer: Optional manufacturer to set
        is_followed: Optional flag to set

    Returns:
        Updated Product or None if product doesn't exist
    """
    with Session(engine) as session:
        db_product = session.get(Product, product.ean)
        if not db_product:
            return None

        if manufacturer is not None:
            db_product.manufacturer = manufacturer
        if is_followed is not None:
            db_product.is_followed = is_followed

        session.commit()
        session.refresh(db_product)
        return db_product


def read_product(engine: Engine, ean: int) -> Optional[Product]:
    """Read a product by its EAN.

    Args:
        engine: SQLAlchemy engine
        ean: European Article Number

    Returns:
        Product instance or None if not found
    """
    with Session(engine) as session:
        product = session.get(Product, ean)
        return product


def read_all_products(engine: Engine) -> List[Product]:
    """Read all products.

    Args:
        engine: SQLAlchemy engine

    Returns:
        List of all products
    """
    with Session(engine) as session:
        products = session.exec(select(Product)).all()
        return list(products)


def delete_product(engine: Engine, ean: int) -> bool:
    """Delete a product by its EAN.

    Args:
        engine: SQLAlchemy engine
        ean: European Article Number

    Returns:
        True if product was deleted, False if not found
    """
    with Session(engine) as session:
        product = session.get(Product, ean)
        if not product:
            return False
        session.delete(product)
        session.commit()
        return True


def create_manufacturer(
    engine: Engine, name: str, website: Optional[str] = None
) -> Manufacturer:
    """Create a new manufacturer.

    Args:
        engine: SQLAlchemy engine
        name: Manufacturer name
        website: Optional manufacturer website

    Returns:
        Created Manufacturer instance
    """
    with Session(engine) as session:
        manufacturer = Manufacturer(name=name, website=website)
        session.add(manufacturer)
        session.commit()
        session.refresh(manufacturer)
        return manufacturer


def read_manufacturer(engine: Engine, id: uuid.UUID) -> Optional[Manufacturer]:
    """Read a manufacturer by its ID.

    Args:
        engine: SQLAlchemy engine
        id: Manufacturer UUID

    Returns:
        Manufacturer instance or None if not found
    """
    with Session(engine) as session:
        manufacturer = session.get(Manufacturer, id)
        return manufacturer


def update_manufacturer(
    engine: Engine,
    manufacturer: Manufacturer,
    name: Optional[str] = None,
    website: Optional[str] = None,
) -> Optional[Manufacturer]:
    """Update an existing manufacturer.

    Args:
        engine: SQLAlchemy engine
        manufacturer: Manufacturer to update
        name: Optional new name
        website: Optional new website

    Returns:
        Updated Manufacturer or None if not found
    """
    with Session(engine) as session:
        db_manufacturer = session.get(Manufacturer, manufacturer.id)
        if not db_manufacturer:
            return None

        if name is not None:
            db_manufacturer.name = name
        if website is not None:
            db_manufacturer.website = website

        session.commit()
        session.refresh(db_manufacturer)
        return db_manufacturer


def delete_manufacturer(engine: Engine, id: uuid.UUID) -> bool:
    """Delete a manufacturer by its ID.

    Args:
        engine: SQLAlchemy engine
        id: Manufacturer UUID

    Returns:
        True if deleted, False if not found
    """
    with Session(engine) as session:
        manufacturer = session.get(Manufacturer, id)
        if not manufacturer:
            return False
        session.delete(manufacturer)
        session.commit()
        return True


def create_store(engine: Engine, name: str, website: Optional[str] = None) -> Store:
    """Create a new store.

    Args:
        engine: SQLAlchemy engine
        name: Store name
        website: Optional store website

    Returns:
        Created Store instance
    """
    with Session(engine) as session:
        store = Store(name=name, website=website)
        session.add(store)
        session.commit()
        session.refresh(store)
        return store


def read_store(engine: Engine, id: uuid.UUID) -> Optional[Store]:
    """Read a store by its ID.

    Args:
        engine: SQLAlchemy engine
        id: Store UUID

    Returns:
        Store instance or None if not found
    """
    with Session(engine) as session:
        store = session.get(Store, id)
        return store


def update_store(
    engine: Engine,
    store: Store,
    name: Optional[str] = None,
    website: Optional[str] = None,
) -> Optional[Store]:
    """Update an existing store.

    Args:
        engine: SQLAlchemy engine
        store: Store to update
        name: Optional new name
        website: Optional new website

    Returns:
        Updated Store or None if not found
    """
    with Session(engine) as session:
        db_store = session.get(Store, store.id)
        if not db_store:
            return None

        if name is not None:
            db_store.name = name
        if website is not None:
            db_store.website = website

        session.commit()
        session.refresh(db_store)
        return db_store


def delete_store(engine: Engine, id: uuid.UUID) -> bool:
    """Delete a store by its ID.

    Args:
        engine: SQLAlchemy engine
        id: Store UUID

    Returns:
        True if deleted, False if not found
    """
    with Session(engine) as session:
        store = session.get(Store, id)
        if not store:
            return False
        session.delete(store)
        session.commit()
        return True


def create_price(engine: Engine, value: float, product: Product, store: Store) -> Price:
    """Create a new price record.

    Args:
        engine: SQLAlchemy engine
        value: Price value
        product: Associated product
        store: Associated store

    Returns:
        Created Price instance
    """
    with Session(engine) as session:
        price = Price(value=value, product=product, store=store)
        session.add(price)
        session.commit()
        session.refresh(price)
        return price


def read_price(engine: Engine, id: uuid.UUID) -> Optional[Price]:
    """Read a price by its ID.

    Args:
        engine: SQLAlchemy engine
        id: Price UUID

    Returns:
        Price instance or None if not found
    """
    with Session(engine) as session:
        price = session.get(Price, id)
        return price


def read_prices_by_product(engine: Engine, product: Product) -> List[Price]:
    """Read all prices for a product.

    Args:
        engine: SQLAlchemy engine
        product: Product to get prices for

    Returns:
        List of Price instances
    """
    with Session(engine) as session:
        db_product = session.get(Product, product.ean)
        if not db_product:
            return []
        return list(db_product.prices)


def read_prices_by_store(engine: Engine, store: Store) -> List[Price]:
    """Read all prices for a store.

    Args:
        engine: SQLAlchemy engine
        store: Store to get prices for

    Returns:
        List of Price instances
    """
    with Session(engine) as session:
        db_store = session.get(Store, store.id)
        if not db_store:
            return []
        return list(db_store.prices)


def read_prices_by_date(engine: Engine, date: datetime) -> List[Price]:
    """Read all prices for a specific date.

    Args:
        engine: SQLAlchemy engine
        date: Date to filter by

    Returns:
        List of Price instances
    """
    with Session(engine) as session:
        prices = session.exec(select(Price).where(Price.date == date)).all()
        return list(prices)


def update_price(
    engine: Engine,
    price: Price,
    value: Optional[float] = None,
    date: Optional[datetime] = None,
    product: Optional[Product] = None,
    store: Optional[Store] = None,
) -> Optional[Price]:
    """Update an existing price.

    Args:
        engine: SQLAlchemy engine
        price: Price to update
        value: Optional new value
        date: Optional new date
        product: Optional new product
        store: Optional new store

    Returns:
        Updated Price or None if not found
    """
    with Session(engine) as session:
        db_price = session.get(Price, price.id)
        if not db_price:
            return None

        if value is not None:
            db_price.value = value
        if date is not None:
            db_price.date = date
        if product is not None:
            db_price.product = product
        if store is not None:
            db_price.store = store

        session.commit()
        session.refresh(db_price)
        return db_price


def delete_price(engine: Engine, id: uuid.UUID) -> bool:
    """Delete a price by its ID.

    Args:
        engine: SQLAlchemy engine
        id: Price UUID

    Returns:
        True if deleted, False if not found
    """
    with Session(engine) as session:
        price = session.get(Price, id)
        if not price:
            return False
        session.delete(price)
        session.commit()
        return True


def create_scrap_data(
    engine: Engine,
    product_name: str,
    manufacturer: Manufacturer,
    weight: int,
    flavour: str,
    type: str,
    age_group: str,
    product: Product,
    composition: str,
    analytical_composition: Optional[str] = None,
    dietary_supplements: Optional[str] = None,
) -> ScrapData:
    """Create a new scrap data record.

    Args:
        engine: SQLAlchemy engine
        product_name: Name of the product
        manufacturer: Associated manufacturer
        weight: Weight in grams
        flavour: Product flavor
        type: Product type
        age_group: Target age group
        product: Associated product
        composition: Product composition
        analytical_composition: Optional analytical composition
        dietary_supplements: Optional dietary supplements

    Returns:
        Created ScrapData instance
    """
    with Session(engine) as session:
        scrap_data = ScrapData(
            product_name=product_name,
            manufacturer=manufacturer,
            weight=weight,
            flavour=flavour,
            type=type,
            age_group=age_group,
            product=product,
            composition=composition,
            analytical_composition=analytical_composition,
            dietary_supplements=dietary_supplements,
        )
        session.add(scrap_data)
        session.commit()
        session.refresh(scrap_data)
        return scrap_data


def read_scrap_data(engine: Engine, id: uuid.UUID) -> Optional[ScrapData]:
    """Read scrap data by its ID.

    Args:
        engine: SQLAlchemy engine
        id: ScrapData UUID

    Returns:
        ScrapData instance or None if not found
    """
    with Session(engine) as session:
        scrap_data = session.get(ScrapData, id)
        return scrap_data


def read_all_valid_scrap_data(engine: Engine) -> List[ScrapData]:
    """Read all valid scrap data.

    Args:
        engine: SQLAlchemy engine

    Returns:
        List of valid ScrapData instances
    """
    with Session(engine) as session:
        scrap_data = session.exec(
            select(ScrapData).where(
                ScrapData.valid_to == None,  # Using == for SQL comparison
                ScrapData.is_valid == True,  # Using == for SQL comparison
            )
        ).all()
        return list(scrap_data)


def read_valid_scrap_data_by_product(
    engine: Engine, product: Product
) -> List[ScrapData]:
    """Read all valid scrap data for a product.

    Args:
        engine: SQLAlchemy engine
        product: Product to get scrap data for

    Returns:
        List of valid ScrapData instances
    """
    with Session(engine) as session:
        db_product = session.get(Product, product.ean)
        if not db_product:
            return []

        scrap_data = session.exec(
            select(ScrapData).where(
                ScrapData.valid_to == None,
                ScrapData.is_valid == True,
                ScrapData.ean == db_product.ean,
            )
        ).all()
        return list(scrap_data)


def update_scrap_data(
    engine: Engine,
    scrap_data: ScrapData,
    product_name: Optional[str] = None,
    manufacturer: Optional[Manufacturer] = None,
    weight: Optional[int] = None,
    flavour: Optional[str] = None,
    type: Optional[str] = None,
    age_group: Optional[str] = None,
    product: Optional[Product] = None,
    composition: Optional[str] = None,
    analytical_composition: Optional[str] = None,
    dietary_supplements: Optional[str] = None,
    valid_to: Optional[datetime] = None,
    is_valid: Optional[bool] = None,
) -> Optional[ScrapData]:
    """Update an existing scrap data record.

    Args:
        engine: SQLAlchemy engine
        scrap_data: ScrapData to update
        product_name: Optional new product name
        manufacturer: Optional new manufacturer
        weight: Optional new weight
        flavour: Optional new flavor
        type: Optional new type
        age_group: Optional new age group
        product: Optional new product
        composition: Optional new composition
        analytical_composition: Optional new analytical composition
        dietary_supplements: Optional new dietary supplements
        valid_to: Optional new valid_to date
        is_valid: Optional new is_valid flag

    Returns:
        Updated ScrapData or None if not found
    """
    with Session(engine) as session:
        db_scrap_data = session.get(ScrapData, scrap_data.id)
        if not db_scrap_data:
            return None

        if product_name is not None:
            db_scrap_data.product_name = product_name
        if manufacturer is not None:
            db_scrap_data.manufacturer = manufacturer
        if weight is not None:
            db_scrap_data.weight = weight
        if flavour is not None:
            db_scrap_data.flavour = flavour
        if type is not None:
            db_scrap_data.type = type
        if age_group is not None:
            db_scrap_data.age_group = age_group
        if product is not None:
            db_scrap_data.product = product
        if composition is not None:
            db_scrap_data.composition = composition
        if analytical_composition is not None:
            db_scrap_data.analytical_composition = analytical_composition
        if dietary_supplements is not None:
            db_scrap_data.dietary_supplements = dietary_supplements
        if valid_to is not None:
            db_scrap_data.valid_to = valid_to
        if is_valid is not None:
            db_scrap_data.is_valid = is_valid

        session.commit()
        session.refresh(db_scrap_data)
        return db_scrap_data


def delete_scrap_data(engine: Engine, id: uuid.UUID) -> bool:
    """Delete scrap data by its ID.

    Args:
        engine: SQLAlchemy engine
        id: ScrapData UUID

    Returns:
        True if deleted, False if not found
    """
    with Session(engine) as session:
        scrap_data = session.get(ScrapData, id)
        if not scrap_data:
            return False
        session.delete(scrap_data)
        session.commit()
        return True


def create_analytical_component(
    engine: Engine,
    name: str,
    value: float,
    scrap_data: ScrapData,
) -> AnalyticalComponent:
    """Create a new analytical component.

    Args:
        engine: SQLAlchemy engine
        name: Component name
        value: Component value
        scrap_data: Associated scrap data

    Returns:
        Created AnalyticalComponent instance
    """
    with Session(engine) as session:
        analytical_component = AnalyticalComponent(
            name=name,
            value=value,
            data_scrap=scrap_data,
        )
        session.add(analytical_component)
        session.commit()
        session.refresh(analytical_component)
        return analytical_component


def read_analytical_component(
    engine: Engine, id: uuid.UUID
) -> Optional[AnalyticalComponent]:
    """Read an analytical component by its ID.

    Args:
        engine: SQLAlchemy engine
        id: AnalyticalComponent UUID

    Returns:
        AnalyticalComponent instance or None if not found
    """
    with Session(engine) as session:
        analytical_component = session.get(AnalyticalComponent, id)
        return analytical_component


def read_analytical_components_by_scrap_data(
    engine: Engine, scrap_data: ScrapData
) -> List[AnalyticalComponent]:
    """Read all analytical components for scrap data.

    Args:
        engine: SQLAlchemy engine
        scrap_data: ScrapData to get components for

    Returns:
        List of AnalyticalComponent instances
    """
    with Session(engine) as session:
        db_scrap_data = session.get(ScrapData, scrap_data.id)
        if not db_scrap_data:
            return []

        analytical_components = session.exec(
            select(AnalyticalComponent).where(
                AnalyticalComponent.data_scrap_id == db_scrap_data.id
            )
        ).all()
        return list(analytical_components)


def update_analytical_component(
    engine: Engine,
    analytical_component: AnalyticalComponent,
    name: Optional[str] = None,
    value: Optional[float] = None,
    scrap_data: Optional[ScrapData] = None,
) -> Optional[AnalyticalComponent]:
    """Update an existing analytical component.

    Args:
        engine: SQLAlchemy engine
        analytical_component: AnalyticalComponent to update
        name: Optional new name
        value: Optional new value
        scrap_data: Optional new scrap data

    Returns:
        Updated AnalyticalComponent or None if not found
    """
    with Session(engine) as session:
        db_component = session.get(AnalyticalComponent, analytical_component.id)
        if not db_component:
            return None

        if name is not None:
            db_component.name = name
        if value is not None:
            db_component.value = value
        if scrap_data is not None:
            db_component.data_scrap = scrap_data

        session.commit()
        session.refresh(db_component)
        return db_component


def delete_analytical_component(engine: Engine, id: uuid.UUID) -> bool:
    """Delete an analytical component by its ID.

    Args:
        engine: SQLAlchemy engine
        id: AnalyticalComponent UUID

    Returns:
        True if deleted, False if not found
    """
    with Session(engine) as session:
        analytical_component = session.get(AnalyticalComponent, id)
        if not analytical_component:
            return False
        session.delete(analytical_component)
        session.commit()
        return True


def create_dietary_component(  # Fixed function name typo
    engine: Engine,
    name: str,
    data_scrap: ScrapData,
    chemical_form: Optional[str] = None,
    value: Optional[float] = None,
    unit: Optional[str] = None,
) -> DietaryComponent:
    """Create a new dietary component.

    Args:
        engine: SQLAlchemy engine
        name: Component name
        data_scrap: Associated scrap data
        chemical_form: Optional chemical form
        value: Optional component value
        unit: Optional unit of measurement

    Returns:
        Created DietaryComponent instance
    """
    with Session(engine) as session:
        dietary_component = DietaryComponent(
            name=name,
            data_scrap=data_scrap,
            chemical_form=chemical_form,
            value=value,
            unit=unit,
        )
        session.add(dietary_component)
        session.commit()
        session.refresh(dietary_component)
        return dietary_component


def read_dietary_component(engine: Engine, id: uuid.UUID) -> Optional[DietaryComponent]:
    """Read a dietary component by its ID.

    Args:
        engine: SQLAlchemy engine
        id: DietaryComponent UUID

    Returns:
        DietaryComponent instance or None if not found
    """
    with Session(engine) as session:
        dietary_component = session.get(DietaryComponent, id)
        return dietary_component


def read_dietary_components_by_scrap_data(
    engine: Engine, scrap_data: ScrapData
) -> List[DietaryComponent]:
    """Read all dietary components for scrap data.

    Args:
        engine: SQLAlchemy engine
        scrap_data: ScrapData to get components for

    Returns:
        List of DietaryComponent instances
    """
    with Session(engine) as session:
        db_scrap_data = session.get(ScrapData, scrap_data.id)
        if not db_scrap_data:
            return []

        dietary_components = session.exec(
            select(DietaryComponent).where(
                DietaryComponent.data_scrap_id == db_scrap_data.id
            )
        ).all()
        return list(dietary_components)


def update_dietary_component(
    engine: Engine,
    dietary_component: DietaryComponent,
    name: Optional[str] = None,
    data_scrap: Optional[ScrapData] = None,
    chemical_form: Optional[str] = None,
    value: Optional[float] = None,
    unit: Optional[str] = None,
) -> Optional[DietaryComponent]:
    """Update an existing dietary component.

    Args:
        engine: SQLAlchemy engine
        dietary_component: DietaryComponent to update
        name: Optional new name
        data_scrap: Optional new scrap data
        chemical_form: Optional new chemical form
        value: Optional new value
        unit: Optional new unit

    Returns:
        Updated DietaryComponent or None if not found
    """
    with Session(engine) as session:
        db_component = session.get(DietaryComponent, dietary_component.id)
        if not db_component:
            return None

        if name is not None:
            db_component.name = name
        if data_scrap is not None:
            db_component.data_scrap = data_scrap
        if chemical_form is not None:
            db_component.chemical_form = chemical_form
        if value is not None:
            db_component.value = value
        if unit is not None:
            db_component.unit = unit

        session.commit()
        session.refresh(db_component)
        return db_component


def delete_dietary_component(engine: Engine, id: uuid.UUID) -> bool:
    """Delete a dietary component by its ID.

    Args:
        engine: SQLAlchemy engine
        id: DietaryComponent UUID

    Returns:
        True if deleted, False if not found
    """
    with Session(engine) as session:
        dietary_component = session.get(DietaryComponent, id)
        if not dietary_component:
            return False
        session.delete(dietary_component)
        session.commit()
        return True
