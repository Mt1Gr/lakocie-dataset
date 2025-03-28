from datetime import datetime
from typing import Sequence
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


def create_store(engine: Engine, name: str, website: str | None) -> Store:
    with Session(engine) as session:
        store = Store(name=name, website=website)
        session.add(store)
        session.commit()
        session.refresh(store)
        return store


def get_or_create_store_by_name(engine: Engine, name: str) -> Store:
    with Session(engine) as session:
        store = session.exec(select(Store).where(Store.name == name)).first()
        if store is None:
            store = create_store(engine, name, None)
        return store


def read_stores(engine: Engine) -> Sequence[Store]:
    with Session(engine) as session:
        stores = session.exec(select(Store)).all()
        return stores


def create_manufacturer(engine: Engine, name: str, website: str | None) -> Manufacturer:
    with Session(engine) as session:
        manufacturer = Manufacturer(name=name, website=website)
        session.add(manufacturer)
        session.commit()
        session.refresh(manufacturer)
        return manufacturer


def get_or_create_manufacturer(engine: Engine, name: str) -> Manufacturer:
    with Session(engine) as session:
        manufacturer = session.exec(
            select(Manufacturer).where(Manufacturer.name == name)
        ).first()
        if manufacturer is None:
            manufacturer = create_manufacturer(engine, name, None)
        return manufacturer


def create_product(engine: Engine, ean: int, manufactuer: Manufacturer) -> Product:
    with Session(engine) as session:
        product = Product(ean=ean, manufacturer_id=manufactuer.id)
        session.add(product)
        session.commit()
        session.refresh(product)
        return product


def get_or_create_product(
    engine: Engine, ean: int, manufacturer: Manufacturer
) -> Product:
    with Session(engine) as session:
        product = session.exec(select(Product).where(Product.ean == ean)).first()
        if product is None:
            product = create_product(engine, ean, manufacturer)
        return product


def read_products(engine: Engine) -> Sequence[Product]:
    with Session(engine) as session:
        products = session.exec(select(Product)).all()
        return products


def update_product(
    engine: Engine,
    product: Product,
    ean: int | None = None,
    manufacturer: Manufacturer | None = None,
    is_followed: bool | None = None,
) -> Product | None:
    with Session(engine) as session:
        db_product = session.get(Product, product.ean)
        if not db_product:
            return None

        if ean is not None:
            db_product.ean = ean
        if manufacturer is not None:
            db_product.manufacturer = manufacturer
        if is_followed is not None:
            db_product.is_followed = is_followed

        session.commit()
        session.refresh(db_product)
        return db_product


def create_price(
    engine: Engine,
    value: float,
    product: Product,
    store: Store,
    date: datetime = datetime.now(),
) -> Price:
    with Session(engine) as session:
        price = Price(
            value=value, product_ean=product.ean, store_id=store.id, date=date
        )
        session.add(price)
        session.commit()
        session.refresh(price)
        return price


def read_price_by_product_store_and_date(
    engine: Engine, product: Product, store: Store, date: datetime
) -> Price | None:
    with Session(engine) as session:
        price = session.exec(
            select(Price)
            .where(Price.product_ean == product.ean)
            .where(Price.store_id == store.id)
            .where(Price.date == date)
        ).first()
        return price


def create_scrap_data(
    engine: Engine,
    product_name: str,
    manyfacturer: Manufacturer,
    weight: int,
    flavour: str,
    type: str,
    age_group: str,
    product: Product,
    composition: str,
    analytical_composition: str | None,
    dietary_supplements: str | None,
    store: Store,
    date: datetime = datetime.now(),
) -> ScrapData:
    with Session(engine) as session:
        scrap_data = ScrapData(
            product_name=product_name,
            manufacturer=manyfacturer,
            weight=weight,
            flavour=flavour,
            type=type,
            age_group=age_group,
            ean=product.ean,
            product=product,
            composition=composition,
            analytical_composition=analytical_composition,
            dietary_supplements=dietary_supplements,
            store=store,
            valid_from=date,
        )
        session.add(scrap_data)
        session.commit()
        session.refresh(scrap_data)
        return scrap_data


def read_valid_scrap_data_by_product_and_store(
    engine: Engine, product: Product, store: Store
) -> ScrapData | None:
    with Session(engine) as session:
        valid_scrap_data = session.exec(
            select(ScrapData)
            .where(ScrapData.is_valid == True)
            .where(ScrapData.ean == product.ean)
            .where(ScrapData.store_id == store.id)
        ).first()
        return valid_scrap_data


def read_all_valid_scrap_data(engine: Engine) -> Sequence[ScrapData]:
    with Session(engine) as session:
        valid_scrap_data = session.exec(
            select(ScrapData).where(ScrapData.is_valid == True)
        ).all()
        return valid_scrap_data


def update_scrap_data(
    engine: Engine,
    scrap_data: ScrapData,
    product_name: str | None = None,
    manufacturer: Manufacturer | None = None,
    weight: int | None = None,
    flavour: str | None = None,
    type: str | None = None,
    age_group: str | None = None,
    product: Product | None = None,
    composition: str | None = None,
    analytical_composition: str | None = None,
    dietary_supplements: str | None = None,
    valid_from: datetime | None = None,
    valid_to: datetime | None = None,
    is_valid: bool | None = None,
    store: Store | None = None,
) -> ScrapData | None:
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
            db_product = session.get(Product, product.ean)
            if db_product:
                db_scrap_data.product = product
        if composition is not None:
            db_scrap_data.composition = composition
        if analytical_composition is not None:
            db_scrap_data.analytical_composition = analytical_composition
        if dietary_supplements is not None:
            db_scrap_data.dietary_supplements = dietary_supplements
        if valid_from is not None:
            db_scrap_data.valid_from = valid_from
        if valid_to is not None:
            db_scrap_data.valid_to = valid_to
        if is_valid is not None:
            db_scrap_data.is_valid = is_valid
        if store is not None:
            db_store = session.get(Store, store.id)
            if db_store:
                db_scrap_data.store = store

        session.commit()
        session.refresh(db_scrap_data)
        return db_scrap_data


def read_scrap_data_by_analytical_comosition(
    engine: Engine, analytical_composition: str
) -> list[ScrapData]:
    with Session(engine) as session:
        scrap_data = session.exec(
            select(ScrapData)
            .where(
                ScrapData.analytical_composition == analytical_composition,
            )
            .where(ScrapData.is_valid == True)
        ).all()
        return [
            ds
            for ds in scrap_data
            if ds.analytical_components == [] and ds.is_valid and ds.product.is_followed
        ]


def read_scrap_data_by_dietary_supplements(
    engine: Engine, dietary_supplements: str
) -> list[ScrapData]:
    with Session(engine) as session:
        scrap_data = session.exec(
            select(ScrapData)
            .where(
                ScrapData.dietary_supplements == dietary_supplements,
            )
            .where(ScrapData.is_valid == True)
        ).all()
        return [
            ds
            for ds in scrap_data
            if ds.dietary_components == [] and ds.is_valid and ds.product.is_followed
        ]


def create_analytical_component(
    engine: Engine, value: float, name: str, scrap_data: ScrapData
) -> AnalyticalComponent:
    with Session(engine) as session:
        analytical_component = AnalyticalComponent(
            value=value, name=name, data_scrap_id=scrap_data.id
        )
        session.add(analytical_component)
        session.commit()
        session.refresh(analytical_component)
        return analytical_component


def create_dietary_component(
    engine: Engine,
    value: float | None,
    unit: str | None,
    name: str,
    chemical_form: str | None,
    scrap_data: ScrapData,
) -> DietaryComponent:
    with Session(engine) as session:
        dietary_component = DietaryComponent(
            value=value,
            unit=unit,
            name=name,
            chemical_form=chemical_form,
            data_scrap_id=scrap_data.id,
        )
        session.add(dietary_component)
        session.commit()
        session.refresh(dietary_component)
        return dietary_component
