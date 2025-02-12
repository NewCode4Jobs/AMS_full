import os
import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from motor.motor_asyncio import AsyncIOMotorDatabase

from backend.app_fastapi.schemas.alarm import AlarmCreate, AlarmResponse
from backend.app_fastapi.repositories.mongo_repository import MongoRepository
from backend.app_fastapi.repositories.postgres_repository import PostgresRepository
from backend.app_fastapi.repositories.sqlite_repository import SQLiteRepository
from backend.app_fastapi.adapters.data_adapter import get_data_adapter

# Get database type from environment variable, default to sqlite
DB_TYPE = os.environ.get('TEST_DB_TYPE', 'sqlite').lower()


@pytest.fixture
def data_adapter():
    """Get the appropriate data adapter based on DB_TYPE"""
    print(f"Running tests for database type: {DB_TYPE}")
    return get_data_adapter(DB_TYPE)


@pytest.fixture
def db_connection(request):
    """Get the appropriate database connection based on DB_TYPE"""
    if DB_TYPE == 'mongodb':
        db = MagicMock(spec=AsyncIOMotorDatabase)
        db.alarms = AsyncMock()
        db.users = AsyncMock()
        return db
    elif DB_TYPE in ['postgres', 'sqlite']:
        db = MagicMock(spec=AsyncSession)
        # Add mock methods to simulate repository methods
        db.execute = AsyncMock()
        db.query = MagicMock()
        db.add = MagicMock()
        db.commit = AsyncMock()
        db.get = AsyncMock()
        db.refresh = MagicMock()
        return db
    else:
        raise ValueError(f"Unsupported database type: {DB_TYPE}")


@pytest.fixture
def repository(db_connection, data_adapter):
    """Get the appropriate repository based on DB_TYPE"""
    if DB_TYPE == 'mongodb':
        return MongoRepository(db_connection, data_adapter)
    elif DB_TYPE == 'postgres':
        return PostgresRepository(db_connection, data_adapter)
    elif DB_TYPE == 'sqlite':
        return SQLiteRepository(db_connection, data_adapter)
    else:
        raise ValueError(f"Unsupported database type: {DB_TYPE}")


@pytest.fixture
def sample_alarm_create():
    return AlarmCreate(
        name="Test Alarm",
        source="system",
        description="Test Description",
        severity="high",
        status="active",
        acknowledged=False
    )


@pytest.mark.asyncio
class TestRepository:
    async def test_create_alarm(self, repository, db_connection, data_adapter, sample_alarm_create):
        # Setup
        if DB_TYPE == 'mongodb':
            inserted_id = "507f1f77bcf86cd799439011"
            db_connection.alarms.insert_one.return_value.inserted_id = inserted_id
            db_connection.alarms.find_one.return_value = {
                "_id": inserted_id,
                "name": sample_alarm_create.name,
                "source": sample_alarm_create.source,
                "description": sample_alarm_create.description,
                "severity": sample_alarm_create.severity,
                "status": sample_alarm_create.status,
                "acknowledged": False
            }
        else:
            # Setup for SQL databases
            db_connection.add.assert_not_called()  # Ensure this is called
            db_connection.execute.return_value.scalar.return_value = 1
            db_connection.get.return_value = {
                "id": 1,
                "name": sample_alarm_create.name,
                "source": sample_alarm_create.source,
                "description": sample_alarm_create.description,
                "severity": sample_alarm_create.severity,
                "status": sample_alarm_create.status,
                "acknowledged": False
            }
        
        # Execute
        result = await repository.create_alarm(sample_alarm_create)
        
        # Assert
        assert isinstance(result, AlarmResponse)
        assert result.name == sample_alarm_create.name
        assert result.description == sample_alarm_create.description
        assert result.severity == sample_alarm_create.severity
        assert not result.acknowledged

    async def test_get_alarm(self, repository, db_connection, data_adapter):
        # Setup
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

    async def test_get_alarm_not_found(self, repository, db_connection, data_adapter):
        # Setup
        if DB_TYPE == 'mongodb':
            db_connection.alarms.find_one.return_value = None
        else:
            db_connection.query.return_value.filter.return_value.first.return_value = None
        
        # Execute
        result = await repository.get_alarm("nonexistent_id")
        
        # Assert
        assert result is None

    async def test_get_all_alarms(self, repository, db_connection, data_adapter):
        # Setup
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
        
        if DB_TYPE == 'mongodb':
            db_connection.alarms.find.return_value.skip.return_value.limit.return_value.to_list.return_value = alarms
        else:
            db_connection.query.return_value.offset.return_value.limit.return_value.all.return_value = alarms
        
        # Execute
        results = await repository.get_all_alarms(skip=0, limit=10)
        
        # Assert
        assert len(results) == 2
        assert all(isinstance(alarm, AlarmResponse) for alarm in results)

    async def test_update_alarm(self, repository, db_connection, data_adapter, sample_alarm_create):
        # Setup
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
        
        if DB_TYPE == 'mongodb':
            db_connection.alarms.find_one_and_update.return_value = updated_data
        else:
            db_connection.query.return_value.filter.return_value.first.return_value = updated_data
        
        # Execute
        result = await repository.update_alarm(alarm_id, sample_alarm_create)
        
        # Assert
        assert isinstance(result, AlarmResponse)
        assert str(result.id) == str(alarm_id)

    async def test_delete_alarm(self, repository, db_connection, data_adapter):
        # Setup
        alarm_id = "507f1f77bcf86cd799439011" if DB_TYPE == 'mongodb' else "1"
        
        if DB_TYPE == 'mongodb':
            db_connection.alarms.delete_one.return_value.deleted_count = 1
        else:
            db_connection.query.return_value.filter.return_value.delete.return_value = 1
        
        # Execute
        result = await repository.delete_alarm(alarm_id)
        
        # Assert
        assert result is True

    async def test_acknowledge_alarm(self, repository, db_connection, data_adapter):
        # Setup
        alarm_id = "507f1f77bcf86cd799439011" if DB_TYPE == 'mongodb' else "1"
        
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
