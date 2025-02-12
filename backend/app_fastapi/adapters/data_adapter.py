from typing import Protocol, Optional, AsyncGenerator, Type, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from bson import ObjectId
from functools import lru_cache
from contextlib import asynccontextmanager

from ..models.alarm import Alarm
from ..core.config import settings


class DataAdapter(Protocol):
    """Protocol defining the data adapter interface."""
    
    async def convert_to_storage_format(self, data: Any) -> dict:
        """Convert domain model to storage format."""
        pass

    async def convert_from_storage_format(self, data: dict) -> Any:
        """Convert storage format to domain model."""
        pass


class MongoDataAdapter(DataAdapter):
    """MongoDB specific data adapter implementation."""
    
    async def convert_to_storage_format(self, alarm: Alarm) -> dict:
        """Convert Alarm model to MongoDB document format."""
        alarm_dict = alarm.dict(exclude_none=True)
        if alarm_dict.get('id'):
            alarm_dict['_id'] = ObjectId(str(alarm_dict.pop('id')))
        return alarm_dict

    async def convert_from_storage_format(self, data: dict) -> Alarm:
        """Convert MongoDB document to Alarm model."""
        if '_id' in data:
            data['id'] = str(data.pop('_id'))
        return Alarm(**data)


class SQLiteDataAdapter(DataAdapter):
    """SQLite specific data adapter implementation."""
    
    async def convert_to_storage_format(self, alarm: Alarm) -> dict:
        return alarm.dict(exclude_none=True)

    async def convert_from_storage_format(self, data: dict) -> Alarm:
        return Alarm(**data)


class PostgresDataAdapter(DataAdapter):
    """PostgreSQL specific data adapter implementation."""
    
    async def convert_to_storage_format(self, alarm: Alarm) -> dict:
        return alarm.dict(exclude_none=True)

    async def convert_from_storage_format(self, data: Any) -> Alarm:
        """Convert storage format to Alarm model.
        
        Args:
            data: Can be a dict, Record object, or SQLAlchemy model instance
        """
        if hasattr(data, '_mapping'):  # asyncpg Record object
            data = dict(data._mapping)
        elif hasattr(data, '__dict__'):  # SQLAlchemy model
            data = {
                k: v for k, v in data.__dict__.items()
                if not k.startswith('_sa_') and k != 'metadata'
            }
        return Alarm(**data)


class DatabaseConfig:
    """Database configuration container."""
    
    def __init__(self, db_type: str, url: str, db_name: str):
        self.db_type = db_type
        self.url = url
        self.db_name = db_name


def create_repository(db_type: str, connection: Any, data_adapter: DataAdapter):
    """
    Factory function to create a repository instance.
    This function should be called by your dependency injection system.
    """
    # Import repositories here to avoid circular imports
    if db_type == "mongodb":
        from ..repositories.mongo_repository import MongoRepository
        return MongoRepository(connection, data_adapter)
    elif db_type == "sqlite":
        from ..repositories.sqlite_repository import SQLiteRepository
        return SQLiteRepository(connection, data_adapter)
    elif db_type == "postgres":
        from ..repositories.postgres_repository import PostgresRepository
        return PostgresRepository(connection, data_adapter)
    else:
        raise ValueError(f"Unsupported database type: {db_type}")


def get_data_adapter(db_type: str) -> DataAdapter:
    """
    Get the appropriate data adapter instance for the specified database type.
    
    Args:
        db_type: Type of database ('mongodb', 'sqlite', or 'postgres')
        
    Returns:
        DataAdapter instance for the specified database type
        
    Raises:
        ValueError: If an unsupported database type is specified
    """
    adapters = {
        "mongodb": MongoDataAdapter,
        "sqlite": SQLiteDataAdapter,
        "postgres": PostgresDataAdapter,
    }
    
    db_type = db_type.lower()
    if db_type not in adapters:
        raise ValueError(f"Unsupported database type: {db_type}")
        
    return adapters[db_type]()


@lru_cache()
def get_db_config() -> DatabaseConfig:
    """Get database configuration from settings."""
    return DatabaseConfig(
        db_type=settings.DB_TYPE,
        url=settings.MONGODB_URL if settings.DB_TYPE == "mongodb" else settings.POSTGRES_URL,
        db_name=settings.MONGODB_DB_NAME if settings.DB_TYPE == "mongodb" else settings.DB_NAME
    )
