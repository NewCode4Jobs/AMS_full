from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class AlarmSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class AlarmBase(BaseModel):
    name: str
    source: str
    severity: AlarmSeverity
    description: str
    status: str
    acknowledged: bool = False

class AlarmCreate(AlarmBase):
    pass

class AlarmResponse(AlarmBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

