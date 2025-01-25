from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models import Alarm, User
from ..schemas import AlarmCreate, AlarmResponse, UserCreate, UserResponse
from .base import BaseRepository

class SQLiteRepository(BaseRepository):
    def __init__(self, db: Session):
        self.db = db

    async def create_alarm(self, alarm: AlarmCreate) -> AlarmResponse:
        try:
            db_alarm = Alarm(
                name=alarm.name,
                description=alarm.description,
                severity=alarm.severity,
                status=alarm.status
            )
            self.db.add(db_alarm)
            self.db.commit()
            self.db.refresh(db_alarm)
            return AlarmResponse.from_orm(db_alarm)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error creating alarm: {str(e)}")

    async def get_alarm(self, alarm_id: int) -> Optional[AlarmResponse]:
        try:
            db_alarm = self.db.query(Alarm).filter(Alarm.id == alarm_id).first()
            return AlarmResponse.from_orm(db_alarm) if db_alarm else None
        except SQLAlchemyError as e:
            raise Exception(f"Error getting alarm: {str(e)}")

    async def list_alarms(self) -> List[AlarmResponse]:
        try:
            alarms = self.db.query(Alarm).all()
            return [AlarmResponse.from_orm(alarm) for alarm in alarms]
        except SQLAlchemyError as e:
            raise Exception(f"Error listing alarms: {str(e)}")

    async def update_alarm(self, alarm_id: int, alarm: AlarmCreate) -> Optional[AlarmResponse]:
        try:
            db_alarm = self.db.query(Alarm).filter(Alarm.id == alarm_id).first()
            if not db_alarm:
                return None
            
            for key, value in alarm.dict().items():
                setattr(db_alarm, key, value)
            
            self.db.commit()
            self.db.refresh(db_alarm)
            return AlarmResponse.from_orm(db_alarm)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error updating alarm: {str(e)}")

    async def delete_alarm(self, alarm_id: int) -> bool:
        try:
            db_alarm = self.db.query(Alarm).filter(Alarm.id == alarm_id).first()
            if not db_alarm:
                return False
            
            self.db.delete(db_alarm)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error deleting alarm: {str(e)}")

    async def create_user(self, user: UserCreate) -> UserResponse:
        try:
            db_user = User(
                username=user.username,
                email=user.email,
                hashed_password=user.password  # TODO: Hash password before storing
            )
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return UserResponse.from_orm(db_user)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error creating user: {str(e)}")

    async def get_user(self, user_id: int) -> Optional[UserResponse]:
        try:
            db_user = self.db.query(User).filter(User.id == user_id).first()
            return UserResponse.from_orm(db_user) if db_user else None
        except SQLAlchemyError as e:
            raise Exception(f"Error getting user: {str(e)}")

    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        try:
            db_user = self.db.query(User).filter(User.email == email).first()
            return UserResponse.from_orm(db_user) if db_user else None
        except SQLAlchemyError as e:
            raise Exception(f"Error getting user by email: {str(e)}")
