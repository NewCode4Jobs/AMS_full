from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path
import os

# Get the project root directory
ROOT_DIR = Path(__file__).parent.parent.parent.parent

# Ensure data directory exists
DATA_DIR = ROOT_DIR / "data"
os.makedirs(DATA_DIR, exist_ok=True)


class Settings(BaseSettings):
    # Database Settings
    DB_TYPE: str = "sqlite"
    
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173", "http://localhost:8080"]
    # SQLite Settings
    SQLITE_DB: str = str(DATA_DIR / "alarm_system.db")
    SQLITE_URL: str = f"sqlite+aiosqlite:///{SQLITE_DB}"
    
    # PostgreSQL Settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "alarm_system"
    POSTGRES_URL: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    
    # MongoDB Settings
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "alarm_system"
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Alarm Management System"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create a singleton instance
settings = Settings()


# For dependency injection if needed
@lru_cache
def get_settings() -> Settings:
    return settings
