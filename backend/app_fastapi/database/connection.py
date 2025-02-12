from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from motor.motor_asyncio import AsyncIOMotorClient
import os

from backend.app_fastapi.core.config import settings

# Create base declarative class for models
Base = declarative_base()

# Async database engine setup
if settings.DB_TYPE == "sqlite":
    # Explicitly use aiosqlite for async SQLite support
    engine = create_async_engine(
        settings.SQLITE_URL, 
        connect_args={"check_same_thread": False},
        echo=True,
        future=True
    )
elif settings.DB_TYPE == "postgres":
    # Use asyncpg for async PostgreSQL support
    engine = create_async_engine(
        settings.POSTGRES_URL, 
        echo=True,
        future=True
    )
else:
    # Placeholder for other database types if needed
    engine = None

# Create async session factory
async_session = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_db():
    """
    Dependency function to get a database session.
    
    Yields:
        AsyncSession: A database session for the current request.
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_mongodb():
    """Get MongoDB database instance."""
    if settings.DB_TYPE == "mongodb":
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        return client[settings.MONGODB_DB_NAME]
    return None

async def init_db():
    """Initialize database based on configuration."""
    if settings.DB_TYPE in ["sqlite", "postgres"]:
        # Create all tables in SQLite/PostgreSQL
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    elif settings.DB_TYPE == "mongodb":
        # Create indexes or initial setup for MongoDB if needed
        mongodb = await get_mongodb()
        if mongodb:
            await mongodb.alarms.create_index("email", unique=True)
