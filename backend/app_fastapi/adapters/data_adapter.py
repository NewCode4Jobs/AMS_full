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
    else:
        raise ValueError(f"Unsupported database type: {db_type}")


def get_data_adapter(db_type: str) -> DataAdapter:
    """Get the appropriate data adapter based on database type."""
    adapters = {
        "mongodb": MongoDataAdapter,
        "sqlite": SQLiteDataAdapter,
    }
    adapter_class = adapters.get(db_type)
    if not adapter_class:
        raise ValueError(f"No adapter found for database type: {db_type}")
    return adapter_class()


@lru_cache()
def get_db_config() -> DatabaseConfig:
    """Get database configuration from settings."""
    return DatabaseConfig(
        db_type=settings.DB_TYPE,
        url=settings.MONGODB_URL if settings.DB_TYPE == "mongodb" else settings.POSTGRES_URL,
        db_name=settings.MONGODB_DB_NAME if settings.DB_TYPE == "mongodb" else settings.DB_NAME
    )
