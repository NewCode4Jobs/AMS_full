import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app_fastapi.database.connection import Base
from backend.app_fastapi.core.config import settings
from backend.app_fastapi.repositories.postgres_repository import PostgresRepository

def get_test_db_engine():
    """Create a PostgreSQL database engine for testing."""
    test_postgres_url = f"{settings.POSTGRES_URL}_test"
    return create_engine(test_postgres_url)

@pytest.fixture(scope="session")
def test_db_engine():
    """Session-level database engine fixture."""
    engine = get_test_db_engine()
    Base.metadata.create_all(bind=engine)
    return engine

@pytest.fixture(scope="function")
def test_db(test_db_engine):
    """Function-level database session fixture."""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db_engine)
    db = SessionLocal()
    
    try:
        # Clear all tables before each test
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()
        
        yield db
    finally:
        db.close()

@pytest.fixture
def test_repository(test_db):
    """Create a PostgreSQL repository for testing."""
    return PostgresRepository(test_db)

@pytest.fixture
def sample_alarm():
    """Provide a sample alarm for PostgreSQL tests."""
    return {
        "name": "Postgres Test Alarm",
        "description": "Postgres Alarm Description",
        "severity": "high",
        "status": "active",
        "source": "application"
    }
