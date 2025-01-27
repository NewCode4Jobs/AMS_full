import pytest
from pydantic import ValidationError
from backend.app_fastapi.schemas.alarm import AlarmCreate, AlarmUpdate, AlarmSeverity

def test_valid_alarm_create():
    alarm_data = {
        "name": "Test Alarm",
        "description": "Test Description",
        "severity": "high",
        "source": "system",
        "status": "active",
        "acknowledged": False
    }
    alarm = AlarmCreate(**alarm_data)
    assert alarm.name == alarm_data["name"]
    assert alarm.severity == AlarmSeverity.HIGH
    assert alarm.source == alarm_data["source"]

def test_invalid_severity_alarm_create():
    alarm_data = {
        "name": "Test Alarm",
        "description": "Test Description",
        "severity": "invalid",  # Invalid severity
        "source": "system",
        "status": "active",
        "acknowledged": False
    }
    with pytest.raises(ValidationError):
        AlarmCreate(**alarm_data)

def test_valid_alarm_update():
    update_data = {
        "name": "Updated Alarm",
        "severity": "critical"
    }
    alarm_update = AlarmUpdate(**update_data)
    assert alarm_update.name == update_data["name"]
    assert alarm_update.severity == AlarmSeverity.CRITICAL
    # Optional fields should be None
    assert alarm_update.source is None
    assert alarm_update.description is None

def test_empty_alarm_update():
    update_data = {}
    alarm_update = AlarmUpdate(**update_data)
    assert all(getattr(alarm_update, field) is None 
              for field in ["name", "description", "severity", "source", "status"])
