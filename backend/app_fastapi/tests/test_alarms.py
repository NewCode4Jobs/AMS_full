import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.fixture
def sample_alarm():
    """Fixture providing a standard sample alarm for testing."""
    return {
        "name": "Test Alarm",
        "source": "system",
        "severity": "high",
        "description": "Test Description",
        "status": "active",
        "acknowledged": False
    }


@pytest.mark.asyncio
async def test_create_alarm(test_app, sample_alarm):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/alarms/", json=sample_alarm)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == sample_alarm["name"]
        assert data["severity"] == sample_alarm["severity"]
        assert "id" in data
        assert "timestamp" in data


@pytest.mark.asyncio
async def test_get_alarms_empty(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/alarms/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []


@pytest.mark.asyncio
async def test_get_alarms_with_data(test_app, sample_alarm):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        # Create an alarm first
        await ac.post("/api/v1/alarms/", json=sample_alarm)

        # Get all alarms
        response = await ac.get("/api/v1/alarms/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == sample_alarm["name"]


@pytest.mark.asyncio
async def test_update_alarm(test_app, sample_alarm):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        # Create an alarm first
        create_response = await ac.post("/api/v1/alarms/", json=sample_alarm)
        alarm_id = create_response.json()["id"]

        # Update the alarm
        update_data = {
            "name": "Updated Alarm",
            "severity": "critical"
        }
        response = await ac.put(f"/api/v1/alarms/{alarm_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["severity"] == update_data["severity"]
        # Check that other fields remain unchanged
        assert data["source"] == sample_alarm["source"]


@pytest.mark.asyncio
async def test_update_nonexistent_alarm(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        update_data = {"name": "Updated Alarm"}
        response = await ac.put("/api/v1/alarms/999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_acknowledge_alarm(test_app, sample_alarm):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        # Create an alarm first
        create_response = await ac.post("/api/v1/alarms/", json=sample_alarm)
        alarm_id = create_response.json()["id"]

        # Acknowledge the alarm
        response = await ac.put(f"/api/v1/alarms/{alarm_id}/acknowledge")
        assert response.status_code == status.HTTP_200_OK

        # Verify the alarm is acknowledged
        get_response = await ac.get("/api/v1/alarms/")
        alarm = get_response.json()[0]
        assert alarm["acknowledged"] is True


@pytest.mark.asyncio
async def test_acknowledge_nonexistent_alarm(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        response = await ac.put("/api/v1/alarms/999/acknowledge")
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_alarm_invalid_severity(test_app, sample_alarm):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        invalid_alarm = sample_alarm.copy()
        invalid_alarm["severity"] = "invalid"
        response = await ac.post("/api/v1/alarms/", json=invalid_alarm)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_alarm_missing_required_field(test_app, sample_alarm):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        invalid_alarm = sample_alarm.copy()
        del invalid_alarm["name"]
        response = await ac.post("/api/v1/alarms/", json=invalid_alarm)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_get_alarm_stats(test_app, sample_alarm):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        # Create multiple alarms with different severities
        alarms = [
            {**sample_alarm, "severity": "critical"},
            {**sample_alarm, "severity": "high"},
            {**sample_alarm, "severity": "medium"},
            {**sample_alarm, "severity": "low"}
        ]

        for alarm in alarms:
            await ac.post("/api/v1/alarms/", json=alarm)

        # Get updated stats
        response = await ac.get("/api/v1/alarms/stats")
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
