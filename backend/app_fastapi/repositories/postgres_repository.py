from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models import Alarm, User
from ..schemas import AlarmCreate, AlarmResponse, UserCreate, UserResponse
from .base import BaseRepository

class PostgresRepository(BaseRepository):
    def __init__(self, db: Session):
        self.db = db

    async def create_alarm(self, alarm: AlarmCreate) -> AlarmResponse:
        try:
            db_alarm = Alarm(**alarm.dict())
            self.db.add(db_alarm)
            self.db.commit()
            self.db.refresh(db_alarm)
            return AlarmResponse.from_orm(db_alarm)
        except SQLAlchemyError:
            self.db.rollback()
            raise

    async def get_alarm(self, alarm_id: int) -> Optional[AlarmResponse]:
        alarm = self.db.query(Alarm).filter(Alarm.id == alarm_id).first()
        return AlarmResponse.from_orm(alarm) if alarm else None

    async def get_all_alarms(self, skip: int = 0, limit: int = 100) -> List[AlarmResponse]:
        alarms = self.db.query(Alarm).offset(skip).limit(limit).all()
        return [AlarmResponse.from_orm(alarm) for alarm in alarms]

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
        except SQLAlchemyError:
            self.db.rollback()
            raise

    async def delete_alarm(self, alarm_id: int) -> bool:
        try:
            result = self.db.query(Alarm).filter(Alarm.id == alarm_id).delete()
            self.db.commit()
            return result > 0
        except SQLAlchemyError:
            self.db.rollback()
            raise

    async def acknowledge_alarm(self, alarm_id: int) -> bool:
        try:
            alarm = self.db.query(Alarm).filter(Alarm.id == alarm_id).first()
            if not alarm:
                return False
            
            alarm.acknowledged = True
            self.db.commit()
            return True
        except SQLAlchemyError:
            self.db.rollback()
            raise

    async def create_user(self, user: UserCreate) -> UserResponse:
        try:
            db_user = User(
                email=user.email,
                username=user.username,
                hashed_password=user.password  # TODO: Hash password
            )
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return UserResponse.from_orm(db_user)
        except SQLAlchemyError:
            self.db.rollback()
            raise

    async def get_user(self, user_id: int) -> Optional[UserResponse]:
        user = self.db.query(User).filter(User.id == user_id).first()
        return UserResponse.from_orm(user) if user else None

    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        user = self.db.query(User).filter(User.email == email).first()
        return UserResponse.from_orm(user) if user else None

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        users = self.db.query(User).offset(skip).limit(limit).all()
        return [UserResponse.from_orm(user) for user in users]
