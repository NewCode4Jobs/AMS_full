from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from ..database.connection import Base

class Alarm(Base):
    __tablename__ = "alarms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    source = Column(String, index=True)
    severity = Column(String, index=True)
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String, index=True)
    acknowledged = Column(Boolean, default=False)
