from sqlmodel import create_engine
from ..config import config

engine = create_engine(f"sqlite:///{config.get_database_path()}")


def init_db():
    from . import schemas

    print("[INFO] Creating database tables")
    schemas.SQLModel.metadata.create_all(
        engine
    )  # does not attempt to recreate tables if they already exist
