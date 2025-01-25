from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ...database.connection import get_db
from ...models.alarm import Alarm
from ...schemas.alarm import AlarmCreate, AlarmResponse

router = APIRouter()

@router.get("/alarms/", response_model=List[AlarmResponse])
def get_alarms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alarms = db.query(Alarm).offset(skip).limit(limit).all()
    return alarms

@router.post("/alarms/", response_model=AlarmResponse)
def create_alarm(alarm: AlarmCreate, db: Session = Depends(get_db)):
    db_alarm = Alarm(**alarm.dict())
    db.add(db_alarm)
    db.commit()
    db.refresh(db_alarm)
    return db_alarm

@router.put("/alarms/{alarm_id}/acknowledge")
def acknowledge_alarm(alarm_id: int, db: Session = Depends(get_db)):
    alarm = db.query(Alarm).filter(Alarm.id == alarm_id).first()
    if not alarm:
        raise HTTPException(status_code=404, detail="Alarm not found")
    
    alarm.acknowledged = True
    db.commit()
    return {"message": "Alarm acknowledged"}
