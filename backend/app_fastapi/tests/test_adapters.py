import pytest
from datetime import datetime, timezone
from bson import ObjectId
from typing import Dict, Any

from backend.app_fastapi.schemas.alarm import AlarmCreate, AlarmResponse
from backend.app_fastapi.adapters.data_adapter import (
    MongoDataAdapter,
    SQLiteDataAdapter,
    PostgresDataAdapter
)

@pytest.fixture
def sample_alarm():
    return AlarmCreate(
        name="Test Alarm",
        source="system",
        severity="high",
        description="Test Description",
        status="active",
        acknowledged=False
    )

def _clean_sqlalchemy_object(obj: Any) -> Dict[str, Any]:
    """
    Clean SQLAlchemy object by removing internal attributes.
    
    Args:
        obj: SQLAlchemy model instance
    
    Returns:
        Dict with clean data
    """
    if hasattr(obj, '__dict__'):
        # Remove SQLAlchemy internal attributes
        return {
            k: v for k, v in obj.__dict__.items() 
            if not k.startswith('_sa_') and k != 'metadata'
        }
    return obj

@pytest.mark.asyncio
class TestMongoDataAdapter:
    async def test_convert_to_storage_format(self, sample_alarm):
        adapter = MongoDataAdapter()
        result = await adapter.convert_to_storage_format(sample_alarm)
        
        assert "_id" not in result  # No ID for create
        assert result["name"] == sample_alarm.name
        assert result["description"] == sample_alarm.description
        assert result["severity"] == sample_alarm.severity
        assert result["acknowledged"] == sample_alarm.acknowledged

    async def test_convert_from_storage_format(self, sample_alarm):
        adapter = MongoDataAdapter()
        mongo_data = {
            "_id": ObjectId("507f1f77bcf86cd799439011"),
            "name": sample_alarm.name,
            "source": sample_alarm.source,
            "description": sample_alarm.description,
            "severity": sample_alarm.severity,
            "status": sample_alarm.status,
            "timestamp": datetime.now(timezone.utc),
            "acknowledged": sample_alarm.acknowledged
        }
        
        result = await adapter.convert_from_storage_format(mongo_data)
        assert isinstance(result, AlarmResponse)
        assert result.id == "507f1f77bcf86cd799439011"
        assert result.name == sample_alarm.name
        assert result.description == sample_alarm.description
        assert result.severity == sample_alarm.severity
        assert result.acknowledged == sample_alarm.acknowledged

@pytest.mark.asyncio
class TestSQLiteDataAdapter:
    async def test_convert_to_storage_format(self, sample_alarm):
        adapter = SQLiteDataAdapter()
        result = await adapter.convert_to_storage_format(sample_alarm)
        
        assert "id" not in result  # No ID for create
        assert result["name"] == sample_alarm.name
        assert result["description"] == sample_alarm.description
        assert result["severity"] == sample_alarm.severity
        assert result["acknowledged"] == sample_alarm.acknowledged

    async def test_convert_from_storage_format(self, sample_alarm):
        adapter = SQLiteDataAdapter()
        sql_data = {
            "id": 1,
            "name": sample_alarm.name,
            "source": sample_alarm.source,
            "description": sample_alarm.description,
            "severity": sample_alarm.severity,
            "status": sample_alarm.status,
            "timestamp": datetime.now(timezone.utc),
            "acknowledged": sample_alarm.acknowledged
        }
        
        result = await adapter.convert_from_storage_format(sql_data)
        assert isinstance(result, AlarmResponse)
        assert result.id == 1
        assert result.name == sample_alarm.name
        assert result.description == sample_alarm.description
        assert result.severity == sample_alarm.severity
        assert result.acknowledged == sample_alarm.acknowledged

@pytest.mark.asyncio
class TestPostgresDataAdapter:
    async def test_convert_to_storage_format(self, sample_alarm):
        adapter = PostgresDataAdapter()
        result = await adapter.convert_to_storage_format(sample_alarm)
        
        assert "id" not in result  # No ID for create
        assert result["name"] == sample_alarm.name
        assert result["description"] == sample_alarm.description
        assert result["severity"] == sample_alarm.severity
        assert result["acknowledged"] == sample_alarm.acknowledged

    async def test_convert_from_storage_format_dict(self, sample_alarm):
        adapter = PostgresDataAdapter()
        pg_data = {
            "id": 1,
            "name": sample_alarm.name,
            "source": sample_alarm.source,
            "description": sample_alarm.description,
            "severity": sample_alarm.severity,
            "status": sample_alarm.status,
            "timestamp": datetime.now(timezone.utc),
            "acknowledged": sample_alarm.acknowledged
        }
        
        result = await adapter.convert_from_storage_format(pg_data)
        assert isinstance(result, AlarmResponse)
        assert result.id == 1
        assert result.name == sample_alarm.name
        assert result.description == sample_alarm.description
        assert result.severity == sample_alarm.severity
        assert result.acknowledged == sample_alarm.acknowledged

    async def test_convert_from_storage_format_record(self, sample_alarm):
        adapter = PostgresDataAdapter()
        
        # Create a mock Record object (similar to what asyncpg returns)
        class Record:
            def __init__(self, data):
                self._mapping = data
        
        pg_data = Record({
            "id": 1,
            "name": sample_alarm.name,
            "source": sample_alarm.source,
            "description": sample_alarm.description,
            "severity": sample_alarm.severity,
            "status": sample_alarm.status,
            "timestamp": datetime.now(timezone.utc),
            "acknowledged": sample_alarm.acknowledged
        })
        
        result = await adapter.convert_from_storage_format(pg_data)
        assert isinstance(result, AlarmResponse)
        assert result.id == 1
        assert result.name == sample_alarm.name
        assert result.description == sample_alarm.description
        assert result.severity == sample_alarm.severity
        assert result.acknowledged == sample_alarm.acknowledged

    async def test_convert_from_storage_format_sqlalchemy(self, sample_alarm):
        adapter = PostgresDataAdapter()
        
        # Create a mock SQLAlchemy model instance
        class SQLAlchemyModel:
            def __init__(self, **kwargs):
                self.__dict__.update(kwargs)
                self._sa_instance_state = "dummy"  # This should be removed
        
        pg_data = SQLAlchemyModel(
            id=1,
            name=sample_alarm.name,
            source=sample_alarm.source,
            description=sample_alarm.description,
            severity=sample_alarm.severity,
            status=sample_alarm.status,
            timestamp=datetime.now(timezone.utc),
            acknowledged=sample_alarm.acknowledged
        )
        
        # Use the clean_sqlalchemy_object function to remove internal attributes
        cleaned_data = _clean_sqlalchemy_object(pg_data)
        
        result = await adapter.convert_from_storage_format(cleaned_data)
        assert isinstance(result, AlarmResponse)
        assert result.id == 1
        assert result.name == sample_alarm.name
        assert result.description == sample_alarm.description
        assert result.severity == sample_alarm.severity
        assert result.acknowledged == sample_alarm.acknowledged
