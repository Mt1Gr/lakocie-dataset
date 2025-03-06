import uuid
from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime
from decimal import Decimal


class ProductGeneralInformation(SQLModel, table=True):
    ean: int = Field(primary_key=True, gt=0)
    name: str
    flavour: str
    price: Decimal = Field(ge=0.0, decimal_places=2)
    mass: int = Field(ge=0)
    composition: str
    analytical_composition: str | None = Field(default=None)
    dietary_supplments: str | None = Field(default=None)
    scrap_date: datetime = Field(default=datetime.now, index=True)

    # Relationships
    age_group_id: uuid.UUID = Field(foreign_key="agegroup.id")
    age_group: "AgeGroup" = Relationship(back_populates="products")

    type_id: uuid.UUID | None = Field(default=None, foreign_key="producttype.id")
    type: "ProductType" = Relationship(back_populates="products")

    analytical_constituents: list["AnalyticalConstituent"] = Relationship(
        back_populates="product"
    )
    dietary_supplements: list["DietarySupplement"] = Relationship(
        back_populates="product"
    )
    manufacturer_id: uuid.UUID = Field(foreign_key="manufacturer.id")
    manufacturer: "Manufacturer" = Relationship(back_populates="products")


class Manufacturer(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    website: str | None = Field(default=None)

    # Relationships
    products: list[ProductGeneralInformation] = Relationship(
        back_populates="manufacturer"
    )
    ratings: list["Rating"] = Relationship(back_populates="manufacturer")


class ProductType(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    info: str | None = Field(default=None)

    # Relationships
    products: list["ProductGeneralInformation"] = Relationship(back_populates="type")


class AgeGroup(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    min_age: int | None = Field(default=None)
    max_age: int | None = Field(default=None)

    # Relationships
    products: list["ProductGeneralInformation"] = Relationship(
        back_populates="age_group"
    )


class AnalyticalConstituent(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_ean: int = Field(foreign_key="productgeneralinformation.ean")
    name: str = Field(index=True)
    value: Decimal = Field(le=100.0, ge=0.0, decimal_places=2)
    scrap_date: datetime = Field(default=datetime.now, index=True)

    # Relationship
    product: "ProductGeneralInformation" = Relationship(
        back_populates="analytical_constituents"
    )


class DietarySupplementDetails(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    chemical_form: str | None = Field(default=None)
    unit: str | None = Field(default=None)
    bioavailability: str | None = Field(default=None)
    recommended_day_dose: str | None = Field(default=None)

    # Relationships
    supplements: list["DietarySupplement"] = Relationship(
        back_populates="supplement_details"
    )


class DietarySupplement(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    product_ean: int = Field(foreign_key="productgeneralinformation.ean")
    quantity: Decimal | None = Field(default=None, ge=0, decimal_places=2)
    details_id: uuid.UUID = Field(foreign_key="dietarysupplementdetails.id")
    scrap_date: datetime = Field(default=datetime.now, index=True)

    # Relationships
    product: "ProductGeneralInformation" = Relationship(
        back_populates="dietary_supplements"
    )
    supplement_details: "DietarySupplementDetails" = Relationship(
        back_populates="supplements"
    )


class FoodExpert(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    website: str

    # Relationships
    ratings: list["Rating"] = Relationship(back_populates="expert")


class Rating(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    grade: int = Field(ge=0, le=6)
    manufacturer_id: uuid.UUID = Field(foreign_key="manufacturer.id")
    expert_id: uuid.UUID = Field(foreign_key="foodexpert.id")
    comment: str | None = Field(default=None)
    scrap_date: datetime = Field(default=datetime.now, index=True)

    # Relationships
    expert: "FoodExpert" = Relationship(back_populates="ratings")
    manufacturer: "Manufacturer" = Relationship(back_populates="ratings")
