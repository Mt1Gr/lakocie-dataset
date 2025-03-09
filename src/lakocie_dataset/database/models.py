from datetime import datetime
import uuid
from sqlmodel import SQLModel, Relationship, Field


class Product(SQLModel, table=True):
    ean: int = Field(primary_key=True, index=True)

    manufacturer_id: uuid.UUID | None = Field(
        default=None, foreign_key="manufacturer.id"
    )
    manufacturer: "Manufacturer" = Relationship(back_populates="products")
    is_followed: bool = Field(default=True)

    prices: list["Price"] = Relationship(back_populates="product")
    data_scraps: list["ScrapData"] = Relationship(back_populates="product")


class Manufacturer(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    name: str
    website: str | None = Field(default=None)

    products: list["Product"] = Relationship(back_populates="manufacturer")
    data_scraps: list["ScrapData"] = Relationship(
        back_populates="manufacturer", cascade_delete=True
    )


class Price(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    value: float = Field(description="[pln]")
    date: datetime = Field(default_factory=datetime.now, index=True)

    product_ean: int | None = Field(default=None, foreign_key="product.ean", index=True)
    product: "Product" = Relationship(back_populates="prices")

    store_id: uuid.UUID | None = Field(default=None, foreign_key="store.id")
    store: "Store" = Relationship(back_populates="prices")


class Store(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    website: str | None = Field(default=None, description="url")

    prices: list["Price"] = Relationship(back_populates="store")


class ScrapData(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    product_name: str

    manufacturer_id: uuid.UUID | None = Field(
        default=None, foreign_key="manufacturer.id"
    )
    manufacturer: "Manufacturer" = Relationship(back_populates="data_scraps")

    weight: int
    flavour: str
    type: str
    age_group: str

    ean: int | None = Field(default=None, foreign_key="product.ean")
    product: "Product" = Relationship(back_populates="data_scraps")

    composition: str
    analytical_composition: str | None = Field(default=None)
    dietary_supplements: str | None = Field(default=None)

    valid_from: datetime = Field(default_factory=datetime.now)
    valid_to: datetime | None = Field(default=None, index=True)
    is_valid: bool = Field(default=True, index=True)

    analytical_components: list["AnalyticalComponent"] = Relationship(
        back_populates="data_scrap"
    )
    dietary_components: list["DietaryComponent"] = Relationship(
        back_populates="data_scrap"
    )


class AnalyticalComponent(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)

    value: float
    name: str

    data_scrap_id: uuid.UUID | None = Field(default=None, foreign_key="scrapdata.id")
    data_scrap: "ScrapData" = Relationship(back_populates="analytical_components")


class DietaryComponent(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)

    value: float | None = Field(default=None)
    unit: str | None = Field(default=None)
    name: str
    chemical_form: str | None = Field(default=None)

    data_scrap_id: uuid.UUID | None = Field(default=None, foreign_key="scrapdata.id")
    data_scrap: "ScrapData" = Relationship(back_populates="dietary_components")
