import pytest
import uuid
from datetime import datetime, timedelta
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.exc import IntegrityError

# Import the models
from lakocie_dataset.database.models import (
    Product,
    Manufacturer,
    Price,
    Store,
    ScrapData,
    AnalyticalComponent,
    DietaryComponent,
)


# Setup in-memory SQLite database for testing
@pytest.fixture
def engine():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(engine):
    with Session(engine) as session:
        yield session


class TestProduct:
    def test_create_product(self, session):
        # Create manufacturer first (required for relationship)
        manufacturer = Manufacturer(
            name="Test Manufacturer", website="https://example.com"
        )
        session.add(manufacturer)
        session.commit()

        # Create product
        product = Product(ean=1234567890123, manufacturer_id=manufacturer.id)
        session.add(product)
        session.commit()

        # Verify product was created and has correct attributes
        db_product = session.query(Product).first()
        assert db_product.ean == 1234567890123
        assert db_product.manufacturer_id == manufacturer.id

    def test_product_relationships(self, session):
        # Create manufacturer
        manufacturer = Manufacturer(name="Test Manufacturer")
        session.add(manufacturer)
        session.commit()

        # Create product
        product = Product(ean=1234567890123, manufacturer_id=manufacturer.id)
        session.add(product)
        session.commit()

        # Create price for the product
        price = Price(value=10.99, product_ean=product.ean)
        session.add(price)

        # Create scrap data for the product
        scrap_data = ScrapData(
            product_name="Test Product",
            manufacturer_id=manufacturer.id,
            weight=500,
            flavour="Chicken",
            type="Dry",
            age_group="Adult",
            ean=product.ean,
            composition="Test composition",
            analytical_composition="Test analytical composition",
        )
        session.add(scrap_data)
        session.commit()

        # Verify relationships
        db_product = session.query(Product).first()
        assert len(db_product.prices) == 1
        assert db_product.prices[0].value == 10.99
        assert len(db_product.data_scraps) == 1
        assert db_product.data_scraps[0].product_name == "Test Product"
        assert db_product.manufacturer.name == "Test Manufacturer"


class TestManufacturer:
    def test_create_manufacturer(self, session):
        manufacturer = Manufacturer(
            name="Test Manufacturer", website="https://example.com"
        )
        session.add(manufacturer)
        session.commit()

        db_manufacturer = session.query(Manufacturer).first()
        assert db_manufacturer.name == "Test Manufacturer"
        assert db_manufacturer.website == "https://example.com"
        assert isinstance(db_manufacturer.id, uuid.UUID)

    def test_manufacturer_with_null_website(self, session):
        # Test that website can be null
        manufacturer = Manufacturer(name="Test Manufacturer")
        session.add(manufacturer)
        session.commit()

        db_manufacturer = session.query(Manufacturer).first()
        assert db_manufacturer.name == "Test Manufacturer"
        assert db_manufacturer.website is None

    def test_manufacturer_relationships(self, session):
        # Create manufacturer
        manufacturer = Manufacturer(name="Test Manufacturer")
        session.add(manufacturer)
        session.commit()

        # Create products for the manufacturer
        product1 = Product(ean=1234567890123, manufacturer_id=manufacturer.id)
        product2 = Product(ean=9876543210987, manufacturer_id=manufacturer.id)
        session.add(product1)
        session.add(product2)

        # Create scrap data for the manufacturer
        scrap_data = ScrapData(
            product_name="Test Product",
            manufacturer_id=manufacturer.id,
            weight=500,
            flavour="Chicken",
            type="Dry",
            age_group="Adult",
            ean=product1.ean,
            composition="Test composition",
        )
        session.add(scrap_data)
        session.commit()

        # Verify relationships
        db_manufacturer = session.query(Manufacturer).first()
        assert len(db_manufacturer.products) == 2
        assert db_manufacturer.products[0].ean in [1234567890123, 9876543210987]
        assert db_manufacturer.products[1].ean in [1234567890123, 9876543210987]
        assert len(db_manufacturer.data_scraps) == 1
        assert db_manufacturer.data_scraps[0].product_name == "Test Product"


class TestPrice:
    def test_create_price(self, session):
        # Create required related entities
        manufacturer = Manufacturer(name="Test Manufacturer")
        session.add(manufacturer)
        session.commit()

        product = Product(ean=1234567890123, manufacturer_id=manufacturer.id)
        session.add(product)

        store = Store(name="Test Store", website="https://teststore.com")
        session.add(store)
        session.commit()

        # Create price
        price = Price(value=19.99, product_ean=product.ean, store_id=store.id)
        session.add(price)
        session.commit()

        # Verify price
        db_price = session.query(Price).first()
        assert db_price.value == 19.99
        assert db_price.product_ean == product.ean
        assert db_price.store_id == store.id
        assert isinstance(db_price.id, uuid.UUID)

    def test_price_relationships(self, session):
        # Create required related entities
        manufacturer = Manufacturer(name="Test Manufacturer")
        session.add(manufacturer)
        session.commit()

        product = Product(ean=1234567890123, manufacturer_id=manufacturer.id)
        session.add(product)

        store = Store(name="Test Store")
        session.add(store)
        session.commit()

        # Create price
        price = Price(value=19.99, product_ean=product.ean, store_id=store.id)
        session.add(price)
        session.commit()

        # Verify relationships
        db_price = session.query(Price).first()
        assert db_price.product.ean == 1234567890123
        assert db_price.store.name == "Test Store"


class TestStore:
    def test_create_store(self, session):
        store = Store(name="Test Store", website="https://teststore.com")
        session.add(store)
        session.commit()

        db_store = session.query(Store).first()
        assert db_store.name == "Test Store"
        assert db_store.website == "https://teststore.com"
        assert isinstance(db_store.id, uuid.UUID)

    def test_store_with_null_website(self, session):
        # Test that website can be null
        store = Store(name="Test Store")
        session.add(store)
        session.commit()

        db_store = session.query(Store).first()
        assert db_store.name == "Test Store"
        assert db_store.website is None

    def test_store_relationships(self, session):
        # Create store
        store = Store(name="Test Store")
        session.add(store)
        session.commit()

        # Create manufacturer and product for the price
        manufacturer = Manufacturer(name="Test Manufacturer")
        session.add(manufacturer)
        session.commit()

        product = Product(ean=1234567890123, manufacturer_id=manufacturer.id)
        session.add(product)
        session.commit()

        # Create prices for the store
        price1 = Price(value=9.99, store_id=store.id, product_ean=product.ean)
        price2 = Price(value=19.99, store_id=store.id, product_ean=product.ean)
        session.add(price1)
        session.add(price2)
        session.commit()

        # Verify relationships
        db_store = session.query(Store).first()
        assert len(db_store.prices) == 2
        assert db_store.prices[0].value in [9.99, 19.99]
        assert db_store.prices[1].value in [9.99, 19.99]


class TestScrapData:
    def test_create_scrap_data(self, session):
        # Create required related entities
        manufacturer = Manufacturer(name="Test Manufacturer")
        session.add(manufacturer)
        session.commit()

        product = Product(ean=1234567890123, manufacturer_id=manufacturer.id)
        session.add(product)
        session.commit()

        # Create scrap data
        scrap_data = ScrapData(
            product_name="Test Product",
            manufacturer_id=manufacturer.id,
            weight=500,
            flavour="Chicken",
            type="Dry",
            age_group="Adult",
            ean=product.ean,
            composition="Test composition",
            analytical_composition="Test analytical composition",
            dietary_supplements="Test dietary supplements",
        )
        session.add(scrap_data)
        session.commit()

        # Verify scrap data
        db_scrap_data = session.query(ScrapData).first()
        assert db_scrap_data.product_name == "Test Product"
        assert db_scrap_data.weight == 500
        assert db_scrap_data.flavour == "Chicken"
        assert db_scrap_data.type == "Dry"
        assert db_scrap_data.age_group == "Adult"
        assert db_scrap_data.composition == "Test composition"
        assert db_scrap_data.analytical_composition == "Test analytical composition"
        assert db_scrap_data.dietary_supplements == "Test dietary supplements"
        assert db_scrap_data.is_valid == True
        assert isinstance(db_scrap_data.id, uuid.UUID)
        assert isinstance(db_scrap_data.valid_from, datetime)
        assert db_scrap_data.valid_to is None

    def test_scrap_data_valid_dates(self, session):
        # Create required related entities
        manufacturer = Manufacturer(name="Test Manufacturer")
        session.add(manufacturer)
        session.commit()

        product = Product(ean=1234567890123, manufacturer_id=manufacturer.id)
        session.add(product)
        session.commit()

        # Create scrap data with specific dates
        now = datetime.now()
        future = now + timedelta(days=30)

        scrap_data = ScrapData(
            product_name="Test Product",
            manufacturer_id=manufacturer.id,
            weight=500,
            flavour="Chicken",
            type="Dry",
            age_group="Adult",
            ean=product.ean,
            composition="Test composition",
            valid_from=now,
            valid_to=future,
            is_valid=False,
        )
        session.add(scrap_data)
        session.commit()

        # Verify dates
        db_scrap_data = session.query(ScrapData).first()
        assert db_scrap_data.valid_from == now
        assert db_scrap_data.valid_to == future
        assert db_scrap_data.is_valid == False

    def test_scrap_data_relationships(self, session):
        # Create required related entities
        manufacturer = Manufacturer(name="Test Manufacturer")
        session.add(manufacturer)
        session.commit()

        product = Product(ean=1234567890123, manufacturer_id=manufacturer.id)
        session.add(product)
        session.commit()

        # Create scrap data
        scrap_data = ScrapData(
            product_name="Test Product",
            manufacturer_id=manufacturer.id,
            weight=500,
            flavour="Chicken",
            type="Dry",
            age_group="Adult",
            ean=product.ean,
            composition="Test composition",
        )
        session.add(scrap_data)
        session.commit()

        # Add analytical components
        analytical_component = AnalyticalComponent(
            name="Protein", value=25.5, data_scrap_id=scrap_data.id
        )
        session.add(analytical_component)

        # Add dietary components
        dietary_component = DietaryComponent(
            name="Vitamin A",
            value=500.0,
            unit="mg",
            chemical_form="Retinol",
            data_scrap_id=scrap_data.id,
        )
        session.add(dietary_component)
        session.commit()

        # Verify relationships
        db_scrap_data = session.query(ScrapData).first()
        assert db_scrap_data.product.ean == 1234567890123
        assert db_scrap_data.manufacturer.name == "Test Manufacturer"
        assert len(db_scrap_data.analytical_components) == 1
        assert db_scrap_data.analytical_components[0].name == "Protein"
        assert db_scrap_data.analytical_components[0].value == 25.5
        assert len(db_scrap_data.dietary_components) == 1
        assert db_scrap_data.dietary_components[0].name == "Vitamin A"
        assert db_scrap_data.dietary_components[0].value == 500.0


class TestAnalyticalComponent:
    def test_create_analytical_component(self, session):
        # Create required related entities
        manufacturer = Manufacturer(name="Test Manufacturer")
        session.add(manufacturer)
        session.commit()

        product = Product(ean=1234567890123, manufacturer_id=manufacturer.id)
        session.add(product)
        session.commit()

        scrap_data = ScrapData(
            product_name="Test Product",
            manufacturer_id=manufacturer.id,
            weight=500,
            flavour="Chicken",
            type="Dry",
            age_group="Adult",
            ean=product.ean,
            composition="Test composition",
        )
        session.add(scrap_data)
        session.commit()

        # Create analytical component
        analytical_component = AnalyticalComponent(
            name="Protein", value=25.5, data_scrap_id=scrap_data.id
        )
        session.add(analytical_component)
        session.commit()

        # Verify component
        db_component = session.query(AnalyticalComponent).first()
        assert db_component.name == "Protein"
        assert db_component.value == 25.5
        assert db_component.data_scrap_id == scrap_data.id
        assert isinstance(db_component.id, uuid.UUID)

    def test_analytical_component_relationship(self, session):
        # Create required related entities
        manufacturer = Manufacturer(name="Test Manufacturer")
        session.add(manufacturer)
        session.commit()

        product = Product(ean=1234567890123, manufacturer_id=manufacturer.id)
        session.add(product)
        session.commit()

        scrap_data = ScrapData(
            product_name="Test Product",
            manufacturer_id=manufacturer.id,
            weight=500,
            flavour="Chicken",
            type="Dry",
            age_group="Adult",
            ean=product.ean,
            composition="Test composition",
        )
        session.add(scrap_data)
        session.commit()

        # Create analytical component
        analytical_component = AnalyticalComponent(
            name="Protein", value=25.5, data_scrap_id=scrap_data.id
        )
        session.add(analytical_component)
        session.commit()

        # Verify relationship
        db_component = session.query(AnalyticalComponent).first()
        assert db_component.data_scrap.id == scrap_data.id
        assert db_component.data_scrap.product_name == "Test Product"


class TestDietaryComponent:
    def test_create_dietary_component(self, session):
        # Create required related entities
        manufacturer = Manufacturer(name="Test Manufacturer")
        session.add(manufacturer)
        session.commit()

        product = Product(ean=1234567890123, manufacturer_id=manufacturer.id)
        session.add(product)
        session.commit()

        scrap_data = ScrapData(
            product_name="Test Product",
            manufacturer_id=manufacturer.id,
            weight=500,
            flavour="Chicken",
            type="Dry",
            age_group="Adult",
            ean=product.ean,
            composition="Test composition",
        )
        session.add(scrap_data)
        session.commit()

        # Create dietary component with all fields
        dietary_component = DietaryComponent(
            name="Vitamin A",
            value=500.0,
            unit="mg",
            chemical_form="Retinol",
            data_scrap_id=scrap_data.id,
        )
        session.add(dietary_component)
        session.commit()

        # Verify component
        db_component = session.query(DietaryComponent).first()
        assert db_component.name == "Vitamin A"
        assert db_component.value == 500.0
        assert db_component.unit == "mg"
        assert db_component.chemical_form == "Retinol"
        assert db_component.data_scrap_id == scrap_data.id
        assert isinstance(db_component.id, uuid.UUID)

    def test_dietary_component_optional_fields(self, session):
        # Create required related entities
        manufacturer = Manufacturer(name="Test Manufacturer")
        session.add(manufacturer)
        session.commit()

        product = Product(ean=1234567890123, manufacturer_id=manufacturer.id)
        session.add(product)
        session.commit()

        scrap_data = ScrapData(
            product_name="Test Product",
            manufacturer_id=manufacturer.id,
            weight=500,
            flavour="Chicken",
            type="Dry",
            age_group="Adult",
            ean=product.ean,
            composition="Test composition",
        )
        session.add(scrap_data)
        session.commit()

        # Create dietary component with only required fields
        dietary_component = DietaryComponent(
            name="Vitamin B", data_scrap_id=scrap_data.id
        )
        session.add(dietary_component)
        session.commit()

        # Verify component
        db_component = session.query(DietaryComponent).first()
        assert db_component.name == "Vitamin B"
        assert db_component.value is None
        assert db_component.unit is None
        assert db_component.chemical_form is None

    def test_dietary_component_relationship(self, session):
        # Create required related entities
        manufacturer = Manufacturer(name="Test Manufacturer")
        session.add(manufacturer)
        session.commit()

        product = Product(ean=1234567890123, manufacturer_id=manufacturer.id)
        session.add(product)
        session.commit()

        scrap_data = ScrapData(
            product_name="Test Product",
            manufacturer_id=manufacturer.id,
            weight=500,
            flavour="Chicken",
            type="Dry",
            age_group="Adult",
            ean=product.ean,
            composition="Test composition",
        )
        session.add(scrap_data)
        session.commit()

        # Create dietary component
        dietary_component = DietaryComponent(
            name="Vitamin C", value=100.0, unit="mg", data_scrap_id=scrap_data.id
        )
        session.add(dietary_component)
        session.commit()

        # Verify relationship
        db_component = session.query(DietaryComponent).first()
        assert db_component.data_scrap.id == scrap_data.id
        assert db_component.data_scrap.product_name == "Test Product"


def test_cascade_delete_manufacturer(session):
    # Create manufacturer
    manufacturer = Manufacturer(name="Test Manufacturer")
    session.add(manufacturer)
    session.commit()

    # Create product
    product = Product(ean=1234567890123, manufacturer_id=manufacturer.id)
    session.add(product)
    session.commit()

    # Create scrap data
    scrap_data = ScrapData(
        product_name="Test Product",
        manufacturer_id=manufacturer.id,
        weight=500,
        flavour="Chicken",
        type="Dry",
        age_group="Adult",
        ean=product.ean,
        composition="Test composition",
    )
    session.add(scrap_data)
    session.commit()

    # Verify data exists
    assert session.query(ScrapData).count() == 1

    # Delete manufacturer - should cascade delete to scrap_data
    session.delete(manufacturer)
    session.commit()

    # Verify scrap data was deleted
    assert session.query(ScrapData).count() == 0
    # Product should still exist as cascade_delete was only specified for data_scraps
    assert session.query(Product).count() == 1


def test_complete_data_model(session):
    """Test creating a complete data model with all entities and relationships."""
    # Create manufacturer
    manufacturer = Manufacturer(name="Pet Food Co", website="https://petfoodco.com")
    session.add(manufacturer)
    session.commit()

    # Create store
    store = Store(name="Pet Shop", website="https://petshop.com")
    session.add(store)
    session.commit()

    # Create product
    product = Product(ean=1234567890123, manufacturer_id=manufacturer.id)
    session.add(product)
    session.commit()

    # Create price
    price = Price(value=29.99, product_ean=product.ean, store_id=store.id)
    session.add(price)
    session.commit()

    # Create scrap data
    scrap_data = ScrapData(
        product_name="Premium Dog Food",
        manufacturer_id=manufacturer.id,
        weight=1000,
        flavour="Beef",
        type="Wet",
        age_group="Senior",
        ean=product.ean,
        composition="Beef, rice, vegetables",
        analytical_composition="Protein, fat, fiber",
        dietary_supplements="Vitamins and minerals",
    )
    session.add(scrap_data)
    session.commit()

    # Create analytical components
    analytical_components = [
        AnalyticalComponent(name="Protein", value=25.0, data_scrap_id=scrap_data.id),
        AnalyticalComponent(name="Fat", value=15.0, data_scrap_id=scrap_data.id),
        AnalyticalComponent(name="Fiber", value=3.5, data_scrap_id=scrap_data.id),
    ]
    for component in analytical_components:
        session.add(component)
    session.commit()

    # Create dietary components
    dietary_components = [
        DietaryComponent(
            name="Vitamin A",
            value=5000.0,
            unit="IU",
            chemical_form="Retinol",
            data_scrap_id=scrap_data.id,
        ),
        DietaryComponent(
            name="Vitamin D",
            value=500.0,
            unit="IU",
            chemical_form="Cholecalciferol",
            data_scrap_id=scrap_data.id,
        ),
        DietaryComponent(
            name="Calcium", value=1.2, unit="g", data_scrap_id=scrap_data.id
        ),
    ]
    for component in dietary_components:
        session.add(component)
    session.commit()

    # Verify the complete model
    # Check product and its relationships
    db_product = session.query(Product).first()
    assert db_product.ean == 1234567890123
    assert db_product.manufacturer.name == "Pet Food Co"
    assert len(db_product.prices) == 1
    assert db_product.prices[0].value == 29.99
    assert len(db_product.data_scraps) == 1
    assert db_product.data_scraps[0].product_name == "Premium Dog Food"

    # Check scrap data and its relationships
    db_scrap_data = session.query(ScrapData).first()
    assert len(db_scrap_data.analytical_components) == 3
    assert len(db_scrap_data.dietary_components) == 3

    # Check store and its relationships
    db_store = session.query(Store).first()
    assert db_store.name == "Pet Shop"
    assert len(db_store.prices) == 1
    assert db_store.prices[0].product.ean == 1234567890123
