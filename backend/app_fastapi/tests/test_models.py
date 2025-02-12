from datetime import datetime
from backend.app_fastapi.models import Alarm
from sqlalchemy import select


def test_alarm_model_creation(test_db):
    alarm = Alarm(
        name="Test Alarm",
        description="Test Description",
        severity="high",
        source="system",
        status="active",
        acknowledged=False
    )
    
    test_db.add(alarm)
    test_db.commit()
    
    # Refresh to get the timestamp
    test_db.refresh(alarm)
    
    assert alarm.id is not None
    assert isinstance(alarm.timestamp, datetime)
    assert alarm.name == "Test Alarm"
    assert alarm.severity == "high"
    assert alarm.source == "system"
    assert alarm.status == "active"
    assert alarm.acknowledged is False


def test_alarm_model_update(test_db):
    # Create an alarm
    alarm = Alarm(
        name="Test Alarm",
        description="Test Description",
        severity="high",
        source="system",
        status="active",
        acknowledged=False
    )
    test_db.add(alarm)
    test_db.commit()
    
    # Update the alarm
    alarm.severity = "critical"
    alarm.acknowledged = True
    test_db.commit()
    
    # Query the alarm
    query = select(Alarm).filter(Alarm.id == alarm.id)
    result = test_db.execute(query)
    updated_alarm = result.scalar_one_or_none()
    assert updated_alarm.severity == "critical"
    assert updated_alarm.acknowledged is True
