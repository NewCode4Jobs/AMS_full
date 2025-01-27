from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional

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

class AlarmUpdate(BaseModel):
    name: Optional[str] = None
    source: Optional[str] = None
    severity: Optional[AlarmSeverity] = None
    description: Optional[str] = None
    status: Optional[str] = None
    acknowledged: Optional[bool] = None

class AlarmResponse(AlarmBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
