from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine
from ..config import config
from .models import (
    Product,
    Manufacturer,
    Price,
    Store,
    ScrapData,
    AnalyticalComponent,
    DietaryComponent,
)


def create_db_and_tables() -> Engine:
    db_path = config.get_database_path()
    db_url = f"sqlite:///{db_path}"
    engine = create_engine(db_url, echo=True)
    SQLModel.metadata.create_all(engine)

    return engine
