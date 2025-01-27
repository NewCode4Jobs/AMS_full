from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient
import os

from backend.app_fastapi.core.config import settings

# SQLite setup
if settings.DB_TYPE == "sqlite":
    engine = create_engine(settings.SQLITE_URL, connect_args={"check_same_thread": False})
# PostgreSQL setup
elif settings.DB_TYPE == "postgres":
    engine = create_engine(settings.POSTGRES_URL)
else:
    engine = None

# SQL Session setup (for SQLite and PostgreSQL)
SessionLocal = None
if engine:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MongoDB setup
if settings.DB_TYPE == "mongodb":
    mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
    mongodb = mongo_client[settings.MONGODB_DB_NAME]
else:
    mongo_client = None
    mongodb = None

def get_db():
    """Get SQL database session (SQLite or PostgreSQL)."""
    if not engine:
        raise Exception("SQL database not configured")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_mongodb():
    """Get MongoDB database instance."""
    if not mongodb:
        raise Exception("MongoDB not configured")
    return mongodb

async def init_db():
    """Initialize database based on configuration."""
    if settings.DB_TYPE in ["sqlite", "postgres"]:
        # Create all tables in SQLite/PostgreSQL
        Base.metadata.create_all(bind=engine)
    elif settings.DB_TYPE == "mongodb":
        # Create indexes or initial setup for MongoDB if needed
        await mongodb.alarms.create_index("email", unique=True)
        await mongodb.users.create_index("email", unique=True)

async def close_db_connections():
    """Close all database connections."""
    if settings.DB_TYPE == "mongodb" and mongo_client:
        mongo_client.close()
    # SQLite/PostgreSQL connections are handled by the session
