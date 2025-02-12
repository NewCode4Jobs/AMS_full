from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from ..models import Alarm, User
from ..schemas import AlarmCreate, AlarmResponse, UserCreate, UserResponse
from .base import AlarmRepository, UserRepository, BaseAlarmRepository, BaseUserRepository
from ..adapters.data_adapter import DataAdapter


class SQLiteRepository(BaseAlarmRepository, BaseUserRepository, AlarmRepository, UserRepository):
    """SQLite repository implementing both alarm and user operations."""
    
    def __init__(self, db: AsyncSession, data_adapter: DataAdapter):
        self.db = db
        self.data_adapter = data_adapter

    def add(self, model):
        """Delegate add operation to the session."""
        self.db.add(model)

    def commit(self):
        """Delegate commit operation to the session."""
        return self.db.commit()

    def execute(self, query):
        """Delegate execute operation to the session."""
        return self.db.execute(query)

    def refresh(self, model):
        """Delegate refresh operation to the session."""
        return self.db.refresh(model)

    async def add_and_commit(self, model):
        """Add and commit a model in a single operation."""
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model

    async def create_alarm(self, alarm: AlarmCreate) -> AlarmResponse:
        try:
            alarm_dict = await self.data_adapter.convert_to_storage_format(alarm)
            db_alarm = Alarm(**alarm_dict)
            await self.add_and_commit(db_alarm)
            return await self.data_adapter.convert_from_storage_format(db_alarm.__dict__)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise Exception(f"Error creating alarm: {str(e)}")

    async def get_alarm(self, alarm_id: str) -> Optional[AlarmResponse]:
        try:
            query = select(Alarm).filter(Alarm.id == int(alarm_id))
            result = await self.db.execute(query)
            db_alarm = result.scalar_one_or_none()
            if db_alarm:
                return await self.data_adapter.convert_from_storage_format(db_alarm.__dict__)
            return None
        except SQLAlchemyError as e:
            raise Exception(f"Error getting alarm: {str(e)}")

    async def get_all_alarms(self, skip: int = 0, limit: int = 100) -> List[AlarmResponse]:
        try:
            query = select(Alarm).offset(skip).limit(limit)
            result = await self.db.execute(query)
            alarms = result.scalars().all()
            return [await self.data_adapter.convert_from_storage_format(alarm.__dict__) for alarm in alarms]
        except SQLAlchemyError as e:
            raise Exception(f"Error listing alarms: {str(e)}")

    async def update_alarm(self, alarm_id: str, alarm: AlarmCreate) -> Optional[AlarmResponse]:
        try:
            query = select(Alarm).filter(Alarm.id == int(alarm_id))
            result = await self.db.execute(query)
            db_alarm = result.scalar_one_or_none()
            
            if not db_alarm:
                return None
            
            alarm_dict = await self.data_adapter.convert_to_storage_format(alarm)
            for key, value in alarm_dict.items():
                setattr(db_alarm, key, value)
            
            await self.db.commit()
            await self.db.refresh(db_alarm)
            return await self.data_adapter.convert_from_storage_format(db_alarm.__dict__)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise Exception(f"Error updating alarm: {str(e)}")

    async def delete_alarm(self, alarm_id: str) -> bool:
        try:
            query = delete(Alarm).filter(Alarm.id == int(alarm_id))
            result = await self.db.execute(query)
            await self.db.commit()
            return result.rowcount > 0
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise Exception(f"Error deleting alarm: {str(e)}")

    async def acknowledge_alarm(self, alarm_id: str) -> bool:
        try:
            query = select(Alarm).filter(Alarm.id == int(alarm_id))
            result = await self.db.execute(query)
            db_alarm = result.scalar_one_or_none()
            
            if not db_alarm:
                return False
            
            db_alarm.acknowledged = True
            await self.db.commit()
            return True
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise Exception(f"Error acknowledging alarm: {str(e)}")

    async def create_user(self, user: UserCreate) -> UserResponse:
        try:
            user_dict = await self.data_adapter.convert_to_storage_format(user)
            db_user = User(**user_dict)
            await self.add_and_commit(db_user)
            return await self.data_adapter.convert_from_storage_format(db_user.__dict__)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise Exception(f"Error creating user: {str(e)}")

    async def get_user(self, user_id: str) -> Optional[UserResponse]:
        try:
            query = select(User).filter(User.id == int(user_id))
            result = await self.db.execute(query)
            db_user = result.scalar_one_or_none()
            if db_user:
                return await self.data_adapter.convert_from_storage_format(db_user.__dict__)
            return None
        except SQLAlchemyError as e:
            raise Exception(f"Error getting user: {str(e)}")

    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        try:
            query = select(User).filter(User.email == email)
            result = await self.db.execute(query)
            db_user = result.scalar_one_or_none()
            if db_user:
                return await self.data_adapter.convert_from_storage_format(db_user.__dict__)
            return None
        except SQLAlchemyError as e:
            raise Exception(f"Error getting user by email: {str(e)}")

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        try:
            query = select(User).offset(skip).limit(limit)
            result = await self.db.execute(query)
            users = result.scalars().all()
            return [await self.data_adapter.convert_from_storage_format(user.__dict__) for user in users]
        except SQLAlchemyError as e:
            raise Exception(f"Error listing users: {str(e)}")
