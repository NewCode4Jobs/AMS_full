import os
import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from backend.app_fastapi.core.config import settings
from backend.app_fastapi.repositories.mongo_repository import MongoRepository

@pytest.fixture(scope="function")
def test_mongo_db():
    """Create a test MongoDB database."""
    test_db_name = f"{settings.MONGODB_DB_NAME}_test"
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[test_db_name]
    
    try:
        yield db
    finally:
        # Drop the test database
        client.drop_database(test_db_name)

@pytest.fixture
def test_repository(test_mongo_db):
    """Create a MongoDB repository for testing."""
    return MongoRepository(test_mongo_db)

@pytest.fixture
def sample_alarm():
    """Provide a sample alarm for MongoDB tests."""
    return {
        "name": "Mongo Test Alarm",
        "description": "Mongo Alarm Description",
        "severity": "critical",
        "status": "active",
        "source": "security"
    }
