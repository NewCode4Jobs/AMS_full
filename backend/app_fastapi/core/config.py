from pydantic_settings import BaseSettings
from typing import Literal
from functools import lru_cache
import os
from pathlib import Path

# Get the project root directory
ROOT_DIR = Path(__file__).parent.parent.parent.parent

class Settings(BaseSettings):
    # Database Settings
    # DB_TYPE: Literal["sqlite", "postgres", "mongodb"] = "sqlite"
    DB_TYPE: str = "sqlite"
    
    # SQLite Settings
    SQLITE_DB: str = str(ROOT_DIR / "data" / "alarm_system.db")
    
    # PostgreSQL Settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "alarm_system"
    
    # MongoDB Settings
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "alarm_system"
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Alarm Management System"

    @property
    def POSTGRES_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def SQLITE_URL(self) -> str:
        # Create data directory if it doesn't exist
        data_dir = ROOT_DIR / "data"
        data_dir.mkdir(exist_ok=True)
        return f"sqlite:///{self.SQLITE_DB}"

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
