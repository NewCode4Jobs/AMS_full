from typing import Protocol, Optional, AsyncGenerator
from sqlalchemy.orm import Session
from motor.motor_asyncio import AsyncIOMotorClient
from functools import lru_cache

from ..models.alarm import Alarm
from ..core.config import settings
from ..database.connection import SessionLocal
from ..repositories.base import BaseRepository
from ..repositories.postgres_repository import PostgresRepository
from ..repositories.sqlite_repository import SQLiteRepository
from ..repositories.mongo_repository import MongoRepository

class DataAdapter(Protocol):
    async def convert_to_storage_format(self, alarm: Alarm) -> dict:
        pass

    async def convert_from_storage_format(self, data: dict) -> Alarm:
        pass

class DatabaseAdapter:
    """Database adapter to manage connections and repository selection."""
    
    def __init__(self):
        self._postgres_engine = None
        self._mongo_client: Optional[AsyncIOMotorClient] = None
        
    async def init_postgres(self) -> None:
        """Initialize PostgreSQL connection."""
        if not self._postgres_engine:
            from sqlalchemy.ext.asyncio import create_async_engine
            self._postgres_engine = create_async_engine(settings.POSTGRES_URL)

    async def init_mongodb(self) -> None:
        """Initialize MongoDB connection."""
        if not self._mongo_client:
            self._mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)

    async def get_repository(self) -> AsyncGenerator[BaseRepository, None]:
        """Get the appropriate repository based on configuration."""
        try:
            if settings.DB_TYPE == "sqlite":
                db = SessionLocal()
                try:
                    yield SQLiteRepository(db)
                finally:
                    db.close()
            elif settings.DB_TYPE == "postgres":
                db = SessionLocal()
                try:
                    yield PostgresRepository(db)
                finally:
                    db.close()
            else:  # mongodb
                if not self._mongo_client:
                    await self.init_mongodb()
                db = self._mongo_client[settings.MONGODB_DB_NAME]
                try:
                    yield MongoRepository(db)
                finally:
                    pass  # MongoDB cleanup if needed
        except Exception as e:
            # Log the error
            print(f"Error getting repository: {e}")
            raise

    async def close(self):
        """Close all database connections."""
        if self._mongo_client:
            self._mongo_client.close()
        if self._postgres_engine:
            await self._postgres_engine.dispose()

@lru_cache()
def get_db_adapter() -> DatabaseAdapter:
    """Get a singleton instance of DatabaseAdapter."""
    return DatabaseAdapter()
