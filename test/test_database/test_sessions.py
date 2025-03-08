import os
import pytest
from unittest.mock import Mock
from sqlalchemy import Engine, inspect
from sqlmodel import SQLModel

# Import the function and models to test
from lakocie_dataset.database.sessions import create_db_and_tables
from lakocie_dataset.database.models import Product, Manufacturer, Price, Store
from lakocie_dataset import config


@pytest.fixture
def mock_config(monkeypatch):
    """Mock config to return a test database path"""
    monkeypatch.setattr(
        "lakocie_dataset.config.config.get_database_path",
        lambda: "test_database.db",
    )


@pytest.fixture
def cleanup_test_db():
    """Remove test database after tests"""
    yield
    if os.path.exists("test_database.db"):
        os.remove("test_database.db")


class TestCreateDbAndTables:
    def test_creates_engine_with_correct_url(self, monkeypatch, mock_config):
        """Test that engine is created with correct URL from config"""
        # Mock create_engine
        mock_engine = Mock(spec=Engine)
        mock_create_engine = Mock(return_value=mock_engine)
        monkeypatch.setattr(
            "lakocie_dataset.database.sessions.create_engine", mock_create_engine
        )

        create_db_and_tables()

        # Verify create_engine was called with correct URL
        mock_create_engine.assert_called_once_with(
            "sqlite:///test_database.db", echo=True
        )

    def test_creates_all_tables(self, monkeypatch, mock_config):
        """Test that SQLModel.metadata.create_all is called with engine"""
        # Mock create_engine and create_all
        mock_engine = Mock(spec=Engine)
        mock_create_engine = Mock(return_value=mock_engine)
        monkeypatch.setattr(
            "lakocie_dataset.database.sessions.create_engine", mock_create_engine
        )

        # Track calls to create_all
        mock_create_all = Mock()
        monkeypatch.setattr(
            "lakocie_dataset.database.sessions.SQLModel.metadata.create_all",
            mock_create_all,
        )

        create_db_and_tables()

        # Verify create_all was called with our engine
        mock_create_all.assert_called_once_with(mock_engine)

    def test_returns_engine(self, mock_config, cleanup_test_db):
        """Test that function returns a valid SQLAlchemy Engine"""
        engine = create_db_and_tables()

        assert isinstance(engine, Engine)

    def test_creates_tables_in_database(self, mock_config, cleanup_test_db):
        """Test that all model tables are actually created in the database"""
        engine = create_db_and_tables()

        # Get inspector to verify tables
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        # Check that all expected tables exist
        model_tables = [
            Product.__tablename__,
            Manufacturer.__tablename__,
            Price.__tablename__,
            Store.__tablename__,
        ]

        for table in model_tables:
            assert table in tables

    def test_handles_different_database_paths(self, monkeypatch, cleanup_test_db):
        """Test that function works with different database paths"""
        # Set a different path
        monkeypatch.setattr(
            "lakocie_dataset.config.config.get_database_path",
            lambda: "different_test.db",
        )

        engine = create_db_and_tables()

        # Verify the engine was created with the correct URL
        assert engine.url.database == "different_test.db"

        # Clean up additional test file
        if os.path.exists("different_test.db"):
            os.remove("different_test.db")
