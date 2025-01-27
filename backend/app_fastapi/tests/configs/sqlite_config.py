import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app_fastapi.database.connection import Base
from backend.app_fastapi.repositories.sqlite_repository import SQLiteRepository

def get_test_db_engine():
    """Create an in-memory SQLite database engine for testing."""
    return create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

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
    """Create a SQLite repository for testing."""
    return SQLiteRepository(test_db)

@pytest.fixture
def sample_alarm():
    """Provide a sample alarm for SQLite tests."""
    return {
        "name": "SQLite Test Alarm",
        "description": "SQLite Alarm Description",
        "severity": "medium",
        "status": "active",
        "source": "system"
    }
