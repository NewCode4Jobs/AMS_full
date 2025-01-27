import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from motor.motor_asyncio import AsyncIOMotorClient
import importlib

# Add parent directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, project_root)

from backend.app_fastapi.database.connection import Base, get_db
from backend.app_fastapi.main import app
from backend.app_fastapi.core.config import settings
from backend.app_fastapi.repositories.sqlite_repository import SQLiteRepository
from backend.app_fastapi.adapters.data_adapter import DatabaseAdapter

# Dynamically choose database type for testing
DB_TYPE = os.environ.get('TEST_DB_TYPE', 'sqlite')

def pytest_configure(config):
    """Configure the test environment based on the selected database type."""
    # Dynamically import the appropriate configuration module
    config_module_name = f'tests.configs.{DB_TYPE}_config'
    try:
        importlib.import_module(config_module_name)
    except ImportError:
        raise ValueError(f"Unsupported database type for testing: {DB_TYPE}")

def get_test_db_engine():
    if DB_TYPE == 'sqlite':
        # In-memory SQLite for testing
        return create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
    elif DB_TYPE == 'postgres':
        # Use a test-specific PostgreSQL database
        test_postgres_url = f"{settings.POSTGRES_URL}_test"
        return create_engine(test_postgres_url)
    elif DB_TYPE == 'mongodb':
        # Use a test-specific MongoDB database
        test_db_name = f"{settings.MONGODB_DB_NAME}_test"
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        return client[test_db_name]
    else:
        raise ValueError(f"Unsupported database type for testing: {DB_TYPE}")

# Global variables to maintain database state across tests
_test_engine = None
_TestingSessionLocal = None

@pytest.fixture(scope="session")
def test_db_engine():
    global _test_engine
    if _test_engine is None:
        _test_engine = get_test_db_engine()
        # Create all tables once for the entire test session
        if DB_TYPE != 'mongodb':
            Base.metadata.create_all(bind=_test_engine)
    return _test_engine

@pytest.fixture(scope="function")
def test_db(test_db_engine):
    global _TestingSessionLocal
    if _TestingSessionLocal is None:
        if DB_TYPE != 'mongodb':
            _TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db_engine)
        else:
            _TestingSessionLocal = test_db_engine
    
    # Create a new session for each test function
    if DB_TYPE != 'mongodb':
        db = _TestingSessionLocal()
    else:
        db = _TestingSessionLocal
    
    try:
        # Clear all tables before each test
        if DB_TYPE != 'mongodb':
            for table in reversed(Base.metadata.sorted_tables):
                db.execute(table.delete())
            db.commit()
        else:
            db.command("dropDatabase")
        
        yield db
    finally:
        if DB_TYPE != 'mongodb':
            db.close()

@pytest.fixture
def test_repository(test_db):
    """Create a test repository with the test database."""
    if DB_TYPE == 'mongodb':
        pytest.skip("MongoDB tests are skipped")
    return SQLiteRepository(test_db)

@pytest.fixture
def client(test_db, test_repository):
    """Create a test client with overridden dependencies."""
    def override_get_db():
        try:
            yield test_db
        finally:
            if DB_TYPE != 'mongodb':
                test_db.close()
    
    def override_get_repository():
        return test_repository
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Import get_repository dynamically to avoid circular import
    from backend.app_fastapi.main import get_repository
    app.dependency_overrides[get_repository] = override_get_repository
    
    client = TestClient(app)
    yield client
    
    # Clear the overrides
    app.dependency_overrides.clear()

@pytest.fixture
def test_mongo_db():
    if DB_TYPE != 'mongodb':
        pytest.skip("MongoDB tests are skipped")
    
    # Use a test-specific MongoDB database
    test_db_name = f"{settings.MONGODB_DB_NAME}_test"
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[test_db_name]
    
    try:
        yield db
    finally:
        # Drop the test database
        client.drop_database(test_db_name)

@pytest.fixture
def sample_alarm():
    return {
        "name": "Test Alarm",
        "description": "Test Alarm Description",
        "severity": "medium",
        "status": "active",
        "source": "system"
    }
