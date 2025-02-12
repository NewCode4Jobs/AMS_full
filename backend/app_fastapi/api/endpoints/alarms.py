from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from ...database.connection import get_db
from ...models.alarm import Alarm
from ...schemas.alarm import AlarmCreate, AlarmResponse, AlarmUpdate
from ...dependencies import get_repository

router = APIRouter()

@router.get("/alarms/", response_model=List[AlarmResponse])
async def get_alarms(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    # Use select() with async session
    query = select(Alarm).offset(skip).limit(limit)
    result = await db.execute(query)
    alarms = result.scalars().all()
    return alarms

@router.post("/alarms/", response_model=AlarmResponse)
async def create_alarm(alarm: AlarmCreate, db: AsyncSession = Depends(get_db)):
    # Convert AlarmCreate to Alarm model
    db_alarm = Alarm(**alarm.model_dump())
    
    # Add and commit the new alarm
    db.add(db_alarm)
    await db.commit()
    await db.refresh(db_alarm)
    
    return db_alarm

@router.put("/alarms/{alarm_id}", response_model=AlarmResponse)
async def update_alarm(alarm_id: int, alarm: AlarmUpdate, db: AsyncSession = Depends(get_db)):
    # Find the existing alarm
    query = select(Alarm).filter(Alarm.id == alarm_id)
    result = await db.execute(query)
    db_alarm = result.scalar_one_or_none()
    
    if not db_alarm:
        raise HTTPException(status_code=404, detail="Alarm not found")
    
    # Update alarm fields
    update_data = alarm.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_alarm, field, value)
    
    await db.commit()
    await db.refresh(db_alarm)
    return db_alarm

@router.put("/alarms/{alarm_id}/acknowledge")
async def acknowledge_alarm(alarm_id: int, db: AsyncSession = Depends(get_db)):
    # Find the existing alarm
    query = select(Alarm).filter(Alarm.id == alarm_id)
    result = await db.execute(query)
    alarm = result.scalar_one_or_none()
    
    if not alarm:
        raise HTTPException(status_code=404, detail="Alarm not found")
    
    # Update acknowledgement status
    alarm.acknowledged = True
    await db.commit()
    
    return {"status": "success", "message": "Alarm acknowledged"}

@router.get("/alarms/stats")
async def get_alarm_stats(repo=Depends(get_repository)):
    # Get all alarms
    alarms = await repo.get_all_alarms()
    
    # Calculate statistics
    total_alarms = len(alarms)
    severity_counts = {
        "critical": len([a for a in alarms if a.severity == "critical"]),
        "high": len([a for a in alarms if a.severity == "high"]),
        "medium": len([a for a in alarms if a.severity == "medium"]),
        "low": len([a for a in alarms if a.severity == "low"])
    }
    
    status_counts = {
        "active": len([a for a in alarms if a.status == "active"]),
        "resolved": len([a for a in alarms if a.status == "resolved"]),
        "acknowledged": len([a for a in alarms if a.acknowledged])
    }
    
    return {
        "total": total_alarms,
        "by_severity": severity_counts,
        "by_status": status_counts
    }
