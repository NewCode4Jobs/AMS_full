import pytest
from fastapi import status

def test_create_alarm(client, sample_alarm):
    response = client.post("/api/v1/alarms/", json=sample_alarm)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == sample_alarm["name"]
    assert data["severity"] == sample_alarm["severity"]
    assert "id" in data
    assert "timestamp" in data

def test_get_alarms_empty(client):
    response = client.get("/api/v1/alarms/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_get_alarms_with_data(client, sample_alarm):
    # Create an alarm first
    client.post("/api/v1/alarms/", json=sample_alarm)
    
    # Get all alarms
    response = client.get("/api/v1/alarms/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == sample_alarm["name"]

def test_update_alarm(client, sample_alarm):
    # Create an alarm first
    create_response = client.post("/api/v1/alarms/", json=sample_alarm)
    alarm_id = create_response.json()["id"]
    
    # Update the alarm
    update_data = {
        "name": "Updated Alarm",
        "severity": "critical"
    }
    response = client.put(f"/api/v1/alarms/{alarm_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["severity"] == update_data["severity"]
    # Check that other fields remain unchanged
    assert data["source"] == sample_alarm["source"]

def test_update_nonexistent_alarm(client):
    update_data = {"name": "Updated Alarm"}
    response = client.put("/api/v1/alarms/999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_acknowledge_alarm(client, sample_alarm):
    # Create an alarm first
    create_response = client.post("/api/v1/alarms/", json=sample_alarm)
    alarm_id = create_response.json()["id"]
    
    # Acknowledge the alarm
    response = client.put(f"/api/v1/alarms/{alarm_id}/acknowledge")
    assert response.status_code == status.HTTP_200_OK
    
    # Verify the alarm is acknowledged
    get_response = client.get("/api/v1/alarms/")
    alarm = get_response.json()[0]
    assert alarm["acknowledged"] is True

def test_acknowledge_nonexistent_alarm(client):
    response = client.put("/api/v1/alarms/999/acknowledge")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_create_alarm_invalid_severity(client, sample_alarm):
    invalid_alarm = sample_alarm.copy()
    invalid_alarm["severity"] = "invalid"
    response = client.post("/api/v1/alarms/", json=invalid_alarm)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_alarm_missing_required_field(client, sample_alarm):
    invalid_alarm = sample_alarm.copy()
    del invalid_alarm["name"]
    response = client.post("/api/v1/alarms/", json=invalid_alarm)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_alarm_stats(client, sample_alarm):
    # Create multiple alarms with different severities
    alarms = [
        {**sample_alarm, "severity": "critical"},
        {**sample_alarm, "severity": "high"},
        {**sample_alarm, "severity": "medium"},
        {**sample_alarm, "severity": "low"}
    ]
    
    for alarm in alarms:
        client.post("/api/v1/alarms/", json=alarm)
    
    # Get updated stats
    response = client.get("/api/v1/alarms/stats")
    assert response.status_code == 200
    stats = response.json()
    
    assert stats["total"] == 4
    assert stats["by_severity"] == {
        "critical": 1,
        "high": 1,
        "medium": 1,
        "low": 1
    }
    assert stats["by_status"]["active"] == 4  # Assuming default status is "active"
