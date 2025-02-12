import os
import sys
import pytest
import pytest_asyncio
from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.testclient import TestClient

# Add parent directory to Python path first
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, project_root)

from backend.app_fastapi.database.connection import Base, get_db
from backend.app_fastapi.main import app
from backend.app_fastapi.core.config import settings
from backend.app_fastapi.repositories.base import AlarmRepository, UserRepository
from backend.app_fastapi.adapters.data_adapter import (
    get_data_adapter,
    DatabaseConfig,
    create_repository
)

# Configure pytest-asyncio to use "asyncio" as the default event loop
pytest_plugins = ("pytest_asyncio",)

# Dynamically choose database type for testing
DB_TYPE = os.environ.get('TEST_DB_TYPE', 'sqlite')

def get_test_config() -> DatabaseConfig:
    """Get test database configuration."""
    if DB_TYPE == 'mongodb':
        return DatabaseConfig(
            db_type='mongodb',
            url='mongodb://localhost:27017',
            db_name='test_db'
        )
    elif DB_TYPE == 'postgres':
        return DatabaseConfig(
            db_type='postgres',
            url='postgresql+asyncpg://localhost/test_db',
            db_name='test_db'
        )
    else:
        return DatabaseConfig(
            db_type='sqlite',
            url='sqlite+aiosqlite:///:memory:',
            db_name='test_db'
        )

class TestDatabaseSession:
    """Wrapper for async database session to provide sync-like interface for testing."""
    
    def __init__(self, async_session):
        self._async_session = async_session
    
    def add(self, model):
        """Add a model to the session."""
        self._async_session.add(model)
    
    async def commit(self):
        """Commit the session asynchronously."""
        await self._async_session.commit()
    
    async def refresh(self, model):
        """Refresh a model asynchronously."""
        await self._async_session.refresh(model)
    
    def query(self, *args, **kwargs):
        """Provide a query method for compatibility."""
        return self._async_session.query(*args, **kwargs)
    
    async def execute(self, query):
        """Execute a query asynchronously."""
        return await self._async_session.execute(query)
    
    async def first(self):
        """Get the first result asynchronously."""
        return await self._async_session.first()

@pytest_asyncio.fixture(scope="function")
async def test_engine():
    """Create test database engine."""
    config = get_test_config()
    if config.db_type == 'mongodb':
        client = AsyncIOMotorClient(config.url)
        db = client[config.db_name]
        yield db
        await client.drop_database(config.db_name)
        client.close()
    else:
        engine = create_async_engine(
            config.url,
            echo=True,
            future=True
        )
        
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        yield engine
        
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def test_session(test_engine):
    """Create test database session."""
    config = get_test_config()
    if config.db_type == 'mongodb':
        yield test_engine
    else:
        async_session = sessionmaker(
            test_engine, 
            class_=AsyncSession, 
            expire_on_commit=False
        )
        async with async_session() as session:
            yield TestDatabaseSession(session)

@pytest_asyncio.fixture(scope="function")
async def repository(test_session) -> AsyncGenerator[AlarmRepository, None]:
    """Create test repository."""
    config = get_test_config()
    data_adapter = get_data_adapter(config.db_type)
    repo = create_repository(config.db_type, test_session, data_adapter)
    yield repo

@pytest_asyncio.fixture(scope="function")
async def test_app(repository) -> FastAPI:
    """Create test FastAPI application."""
    async def override_get_repository():
        yield repository
    
    app.dependency_overrides[get_db] = override_get_repository
    yield app
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def client(test_app) -> Generator[TestClient, None, None]:
    """Create test client."""
    yield TestClient(test_app)
