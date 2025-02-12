from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models import Alarm, User
from ..schemas import AlarmCreate, AlarmResponse, UserCreate, UserResponse
from .base import BaseRepository
from ..adapters.data_adapter import get_data_adapter


class SQLiteRepository(BaseRepository):
    def __init__(self, db: Session):
        self.db = db
        self.data_adapter = get_data_adapter()

    async def create_alarm(self, alarm: AlarmCreate) -> AlarmResponse:
        try:
            alarm_dict = await self.data_adapter.convert_to_storage_format(alarm)
            db_alarm = Alarm(**alarm_dict)
            self.db.add(db_alarm)
            self.db.commit()
            self.db.refresh(db_alarm)
            return await self.data_adapter.convert_from_storage_format(db_alarm.__dict__)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error creating alarm: {str(e)}")

    async def get_alarm(self, alarm_id: int) -> Optional[AlarmResponse]:
        try:
            db_alarm = self.db.query(Alarm).filter(Alarm.id == alarm_id).first()
            if db_alarm:
                return await self.data_adapter.convert_from_storage_format(db_alarm.__dict__)
            return None
        except SQLAlchemyError as e:
            raise Exception(f"Error getting alarm: {str(e)}")

    async def list_alarms(self) -> List[AlarmResponse]:
        try:
            alarms = self.db.query(Alarm).all()
            return [await self.data_adapter.convert_from_storage_format(alarm.__dict__) for alarm in alarms]
        except SQLAlchemyError as e:
            raise Exception(f"Error listing alarms: {str(e)}")

    async def update_alarm(self, alarm_id: int, alarm: AlarmCreate) -> Optional[AlarmResponse]:
        try:
            db_alarm = self.db.query(Alarm).filter(Alarm.id == alarm_id).first()
            if not db_alarm:
                return None
            
            alarm_dict = await self.data_adapter.convert_to_storage_format(alarm)
            for key, value in alarm_dict.items():
                setattr(db_alarm, key, value)
            
            self.db.commit()
            self.db.refresh(db_alarm)
            return await self.data_adapter.convert_from_storage_format(db_alarm.__dict__)
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
            user_dict = await self.data_adapter.convert_to_storage_format(user)
            db_user = User(**user_dict)
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return await self.data_adapter.convert_from_storage_format(db_user.__dict__)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error creating user: {str(e)}")

    async def get_user(self, user_id: int) -> Optional[UserResponse]:
        try:
            db_user = self.db.query(User).filter(User.id == user_id).first()
            if db_user:
                return await self.data_adapter.convert_from_storage_format(db_user.__dict__)
            return None
        except SQLAlchemyError as e:
            raise Exception(f"Error getting user: {str(e)}")

    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        try:
            db_user = self.db.query(User).filter(User.email == email).first()
            if db_user:
                return await self.data_adapter.convert_from_storage_format(db_user.__dict__)
            return None
        except SQLAlchemyError as e:
            raise Exception(f"Error getting user by email: {str(e)}")

    async def get_all_alarms(self, skip: int = 0, limit: int = 100) -> List[AlarmResponse]:
        try:
            alarms = self.db.query(Alarm).offset(skip).limit(limit).all()
            return [await self.data_adapter.convert_from_storage_format(alarm.__dict__) for alarm in alarms]
        except SQLAlchemyError as e:
            raise Exception(f"Error getting all alarms: {str(e)}")

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        try:
            users = self.db.query(User).offset(skip).limit(limit).all()
            return [await self.data_adapter.convert_from_storage_format(user.__dict__) for user in users]
        except SQLAlchemyError as e:
            raise Exception(f"Error getting all users: {str(e)}")

    async def acknowledge_alarm(self, alarm_id: int) -> Optional[AlarmResponse]:
        try:
            db_alarm = self.db.query(Alarm).filter(Alarm.id == alarm_id).first()
            if not db_alarm:
                return None
            
            db_alarm.status = "acknowledged"
            self.db.commit()
            self.db.refresh(db_alarm)
            return await self.data_adapter.convert_from_storage_format(db_alarm.__dict__)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error acknowledging alarm: {str(e)}")
