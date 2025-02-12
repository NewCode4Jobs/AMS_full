from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from functools import lru_cache
from typing import Union

from backend.app_fastapi.adapters.data_adapter import (
    get_data_adapter, 
    get_db_config, 
    create_repository
)
from backend.app_fastapi.core.config import settings
from backend.app_fastapi.database.connection import get_db, get_mongodb
from .repositories.base import AlarmRepository, UserRepository


async def get_db_connection():
    """Get database connection based on configuration."""
    config = get_db_config()
    if config.db_type == "mongodb":
        client = AsyncIOMotorClient(config.connection_string)
        return client[config.db_name]
    elif config.db_type == "postgres":
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.orm import sessionmaker
        from .database.connection import Base
        
        engine = create_async_engine(
            config.connection_string,
            echo=True,
            future=True
        )
        
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        return async_session()
    elif config.db_type == "sqlite":
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.orm import sessionmaker
        from .database.connection import Base
        
        engine = create_async_engine(
            config.connection_string,
            echo=True,
            future=True
        )
        
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        return async_session()
    else:
        raise ValueError(f"Unsupported database type: {config.db_type}")


@lru_cache()
def get_repository():
    """
    Get the appropriate repository based on database configuration.
    
    Returns:
        Repository instance for the configured database type.
    """
    # Determine database connection based on configuration
    if settings.DB_TYPE == "mongodb":
        connection = get_mongodb()
    else:
        # For SQLite and PostgreSQL, use the async database session
        connection = get_db().__anext__()
    
    # Get the appropriate data adapter
    data_adapter = get_data_adapter(settings.DB_TYPE)
    
    # Create and return the repository
    return create_repository(settings.DB_TYPE, connection, data_adapter)


@asynccontextmanager
async def get_async_repository() -> AsyncGenerator[AlarmRepository, None]:
    """
    Dependency function to get the appropriate repository based on configuration.
    
    This function is used as a dependency in FastAPI route handlers to provide
    a dynamically selected repository instance with proper dependency injection.
    
    Yields:
        AlarmRepository: A repository instance for the configured database type
    """
    config = get_db_config()
    connection = await get_db_connection()
    data_adapter = get_data_adapter(config.db_type)
    
    try:
        repo = create_repository(config.db_type, connection, data_adapter)
        yield repo
    finally:
        if hasattr(connection, 'close'):
            await connection.close()
