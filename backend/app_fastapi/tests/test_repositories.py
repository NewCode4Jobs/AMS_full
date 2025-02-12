import os
import pytest
from unittest.mock import AsyncMock, MagicMock
from typing import Dict, Any

from backend.app_fastapi.schemas.alarm import AlarmCreate, AlarmResponse
from backend.app_fastapi.repositories.mongo_repository import MongoRepository
from backend.app_fastapi.repositories.postgres_repository import PostgresRepository
from backend.app_fastapi.repositories.sqlite_repository import SQLiteRepository
from backend.app_fastapi.adapters.data_adapter import get_data_adapter

# Configuration
DB_TYPE = os.environ.get('TEST_DB_TYPE', 'sqlite').lower()


class DatabaseMockFactory:
    """Factory for creating database connection mocks based on database type."""
    
    @staticmethod
    def create_mock(db_type: str):
        """
        Create a mock database connection based on the database type.
        
        Args:
            db_type (str): Type of database (mongodb, postgres, sqlite)
        
        Returns:
            MagicMock: A mock database connection
        """
        if db_type == 'mongodb':
            from motor.motor_asyncio import AsyncIOMotorDatabase
            db_mock = MagicMock(spec=AsyncIOMotorDatabase)
            db_mock.alarms = AsyncMock()
            db_mock.users = AsyncMock()
            return db_mock
        
        elif db_type in ['postgres', 'sqlite']:
            from sqlalchemy.ext.asyncio import AsyncSession
            db_mock = MagicMock(spec=AsyncSession)
            db_mock.execute = AsyncMock()
            db_mock.query = MagicMock()
            db_mock.add = MagicMock()
            db_mock.commit = AsyncMock()
            db_mock.refresh = MagicMock()
            return db_mock
        
        raise ValueError(f"Unsupported database type: {db_type}")


@pytest.fixture
def data_adapter():
    """Get the appropriate data adapter based on DB_TYPE"""
    return get_data_adapter(DB_TYPE)


@pytest.fixture
def db_connection():
    """Get a mock database connection"""
    return DatabaseMockFactory.create_mock(DB_TYPE)


@pytest.fixture
def repository(db_connection, data_adapter):
    """Get the appropriate repository based on DB_TYPE"""
    repositories = {
        'mongodb': MongoRepository,
        'postgres': PostgresRepository,
        'sqlite': SQLiteRepository
    }
    
    if DB_TYPE not in repositories:
        raise ValueError(f"Unsupported database type: {DB_TYPE}")
    
    return repositories[DB_TYPE](db_connection, data_adapter)


@pytest.fixture
def sample_alarm_create():
    """Create a sample alarm for testing"""
    return AlarmCreate(
        name="Test Alarm",
        source="system",
        description="Test Description",
        severity="high",
        status="active",
        acknowledged=False
    )


@pytest.mark.asyncio
class TestRepositoryBase:
    """Base test class for repository operations"""
    
    async def _mock_mongodb_create(self, db_connection, sample_alarm_create):
        """Mock create operation for MongoDB"""
        inserted_id = "507f1f77bcf86cd799439011"
        db_connection.alarms.insert_one.return_value.inserted_id = inserted_id
        db_connection.alarms.find_one.return_value = {
            "_id": inserted_id,
            **sample_alarm_create.model_dump(),
            "acknowledged": False
        }
        return inserted_id
    
    async def _mock_sql_create(self, db_connection, sample_alarm_create):
        """Mock create operation for SQL databases"""
        db_connection.add.assert_not_called()
        db_connection.execute.return_value.scalar.return_value = 1
        db_connection.query.return_value.filter.return_value.first.return_value = {
            "id": 1,
            **sample_alarm_create.model_dump(),
            "acknowledged": False
        }
        return "1"
    
    async def test_create_alarm(self, repository, db_connection, sample_alarm_create):
        """Test creating an alarm"""
        # Prepare mock data
        alarm_id = (await self._mock_mongodb_create(db_connection, sample_alarm_create) 
                    if DB_TYPE == 'mongodb' 
                    else await self._mock_sql_create(db_connection, sample_alarm_create))
        
        # Execute
        result = await repository.create_alarm(sample_alarm_create)
        
        # Assert
        assert isinstance(result, AlarmResponse)
        assert result.name == sample_alarm_create.name
        assert result.description == sample_alarm_create.description
        assert result.severity == sample_alarm_create.severity
        assert not result.acknowledged
    
    async def test_get_alarm(self, repository, db_connection):
        """Test retrieving a single alarm"""
        # Prepare mock data
        alarm_id = "507f1f77bcf86cd799439011" if DB_TYPE == 'mongodb' else "1"
        alarm_data = {
            "_id" if DB_TYPE == 'mongodb' else "id": alarm_id,
            "name": "Test Alarm",
            "source": "system",
            "description": "Test Description",
            "severity": "high",
            "status": "active",
            "acknowledged": False
        }
        
        # Set up mock based on database type
        if DB_TYPE == 'mongodb':
            db_connection.alarms.find_one.return_value = alarm_data
        else:
            db_connection.query.return_value.filter.return_value.first.return_value = alarm_data
        
        # Execute
        result = await repository.get_alarm(alarm_id)
        
        # Assert
        assert isinstance(result, AlarmResponse)
        assert str(result.id) == str(alarm_id)
        assert result.name == "Test Alarm"
    
    async def test_get_alarm_not_found(self, repository, db_connection):
        """Test retrieving a non-existent alarm"""
        # Set up mock to return None
        if DB_TYPE == 'mongodb':
            db_connection.alarms.find_one.return_value = None
        else:
            db_connection.query.return_value.filter.return_value.first.return_value = None
        
        # Execute
        result = await repository.get_alarm("nonexistent_id")
        
        # Assert
        assert result is None
    
    async def test_get_all_alarms(self, repository, db_connection):
        """Test retrieving multiple alarms"""
        # Prepare mock data
        alarms = [
            {
                "_id" if DB_TYPE == 'mongodb' else "id": "1",
                "name": "Alarm 1",
                "source": "system",
                "description": "Description 1",
                "severity": "high",
                "status": "active",
                "acknowledged": False
            },
            {
                "_id" if DB_TYPE == 'mongodb' else "id": "2",
                "name": "Alarm 2",
                "source": "system",
                "description": "Description 2",
                "severity": "medium",
                "status": "active",
                "acknowledged": True
            }
        ]
        
        # Set up mock based on database type
        if DB_TYPE == 'mongodb':
            db_connection.alarms.find.return_value.skip.return_value.limit.return_value.to_list.return_value = alarms
        else:
            db_connection.query.return_value.offset.return_value.limit.return_value.all.return_value = alarms
        
        # Execute
        results = await repository.get_all_alarms(skip=0, limit=10)
        
        # Assert
        assert len(results) == 2
        assert all(isinstance(alarm, AlarmResponse) for alarm in results)
    
    async def test_update_alarm(self, repository, db_connection, sample_alarm_create):
        """Test updating an alarm"""
        # Prepare mock data
        alarm_id = "507f1f77bcf86cd799439011" if DB_TYPE == 'mongodb' else "1"
        updated_data = {
            "_id" if DB_TYPE == 'mongodb' else "id": alarm_id,
            "name": "Updated Alarm",
            "source": "system",
            "description": "Updated Description",
            "severity": "low",
            "status": "resolved",
            "acknowledged": True
        }
        
        # Set up mock based on database type
        if DB_TYPE == 'mongodb':
            db_connection.alarms.find_one_and_update.return_value = updated_data
        else:
            db_connection.query.return_value.filter.return_value.first.return_value = updated_data
        
        # Execute
        result = await repository.update_alarm(alarm_id, sample_alarm_create)
        
        # Assert
        assert isinstance(result, AlarmResponse)
        assert str(result.id) == str(alarm_id)
    
    async def test_delete_alarm(self, repository, db_connection):
        """Test deleting an alarm"""
        # Prepare mock data
        alarm_id = "507f1f77bcf86cd799439011" if DB_TYPE == 'mongodb' else "1"
        
        # Set up mock based on database type
        if DB_TYPE == 'mongodb':
            db_connection.alarms.delete_one.return_value.deleted_count = 1
        else:
            db_connection.query.return_value.filter.return_value.delete.return_value = 1
        
        # Execute
        result = await repository.delete_alarm(alarm_id)
        
        # Assert
        assert result is True
    
    async def test_acknowledge_alarm(self, repository, db_connection):
        """Test acknowledging an alarm"""
        # Prepare mock data
        alarm_id = "507f1f77bcf86cd799439011" if DB_TYPE == 'mongodb' else "1"
        
        # Set up mock based on database type
        if DB_TYPE == 'mongodb':
            db_connection.alarms.update_one.return_value.modified_count = 1
        else:
            db_connection.query.return_value.filter.return_value.first.return_value = {
                "id": alarm_id,
                "acknowledged": True
            }
        
        # Execute
        result = await repository.acknowledge_alarm(alarm_id)
        
        # Assert
        assert result is True
    
    async def test_unacknowledge_alarm(self, repository, db_connection):
        """Test unacknowledging an alarm"""
        # Prepare mock data
        alarm_id = "507f1f77bcf86cd799439011" if DB_TYPE == 'mongodb' else "1"
        
        # Set up mock based on database type
        if DB_TYPE == 'mongodb':
            db_connection.alarms.update_one.return_value.modified_count = 1
        else:
            db_connection.query.return_value.filter.return_value.first.return_value = {
                "id": alarm_id,
                "acknowledged": False
            }
        
        # Execute
        result = await repository.unacknowledge_alarm(alarm_id)
        
        # Assert
        assert result is True
    
    async def test_resolve_alarm(self, repository, db_connection):
        """Test resolving an alarm"""
        # Prepare mock data
        alarm_id = "507f1f77bcf86cd799439011" if DB_TYPE == 'mongodb' else "1"
        
        # Set up mock based on database type
        if DB_TYPE == 'mongodb':
            db_connection.alarms.update_one.return_value.modified_count = 1
        else:
            db_connection.query.return_value.filter.return_value.first.return_value = {
                "id": alarm_id,
                "status": "resolved"
            }
        
        # Execute
        result = await repository.resolve_alarm(alarm_id)
        
        # Assert
        assert result is True
    
    async def test_activate_alarm(self, repository, db_connection):
        """Test activating an alarm"""
        # Prepare mock data
        alarm_id = "507f1f77bcf86cd799439011" if DB_TYPE == 'mongodb' else "1"
        
        # Set up mock based on database type
        if DB_TYPE == 'mongodb':
            db_connection.alarms.update_one.return_value.modified_count = 1
        else:
            db_connection.query.return_value.filter.return_value.first.return_value = {
                "id": alarm_id,
                "status": "active"
            }
        
        # Execute
        result = await repository.activate_alarm(alarm_id)
        
        # Assert
        assert result is True
