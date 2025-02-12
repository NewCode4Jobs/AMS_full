from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from .adapters.data_adapter import get_data_adapter, get_db_config, create_repository
from .repositories.base import BaseRepository


async def get_db_connection():
    """Get database connection based on configuration."""
    config = get_db_config()
    if config.db_type == "mongodb":
        client = AsyncIOMotorClient(config.url)
        return client[config.db_name]
    else:
        # Add other database connections here
        raise ValueError(f"Unsupported database type: {config.db_type}")


@asynccontextmanager
async def get_repository() -> AsyncGenerator[BaseRepository, None]:
    """
    Dependency function to get the appropriate repository based on configuration.
    
    This function is used as a dependency in FastAPI route handlers to provide
    a dynamically selected repository instance with proper dependency injection.
    
    Yields:
        BaseRepository: A repository instance for the configured database type
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
