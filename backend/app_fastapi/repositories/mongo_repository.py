from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timezone
from bson import ObjectId
from ..schemas import AlarmCreate, AlarmResponse, UserCreate, UserResponse
from .base import AlarmRepository, UserRepository, BaseAlarmRepository, BaseUserRepository
from ..adapters.data_adapter import DataAdapter


class MongoRepository(BaseAlarmRepository, BaseUserRepository, AlarmRepository, UserRepository):
    """MongoDB repository implementing both alarm and user operations."""
    
    def __init__(self, db: AsyncIOMotorDatabase, data_adapter: DataAdapter):
        """
        Initialize MongoDB repository with database connection and data adapter.
        
        Args:
            db: MongoDB database connection
            data_adapter: Adapter for data transformations
        """
        self.db = db
        self.alarms_collection = db.alarms
        self.users_collection = db.users
        self.data_adapter = data_adapter

    async def create_alarm(self, alarm: AlarmCreate) -> AlarmResponse:
        alarm_dict = await self.data_adapter.convert_to_storage_format(alarm)
        alarm_dict["timestamp"] = datetime.now(timezone.utc)
        result = await self.alarms_collection.insert_one(alarm_dict)
        created_alarm = await self.alarms_collection.find_one({"_id": result.inserted_id})
        return await self.data_adapter.convert_from_storage_format(created_alarm)

    async def get_alarm(self, alarm_id: str) -> Optional[AlarmResponse]:
        try:
            alarm = await self.alarms_collection.find_one({"_id": ObjectId(alarm_id)})
            if alarm:
                return await self.data_adapter.convert_from_storage_format(alarm)
            return None
        except:
            return None

    async def get_all_alarms(self, skip: int = 0, limit: int = 100) -> List[AlarmResponse]:
        cursor = self.alarms_collection.find().skip(skip).limit(limit)
        alarms = []
        async for alarm in cursor:
            converted_alarm = await self.data_adapter.convert_from_storage_format(alarm)
            alarms.append(converted_alarm)
        return alarms

    async def update_alarm(self, alarm_id: str, alarm: AlarmCreate) -> Optional[AlarmResponse]:
        alarm_dict = await self.data_adapter.convert_to_storage_format(alarm)
        result = await self.alarms_collection.update_one(
            {"_id": ObjectId(alarm_id)},
            {"$set": alarm_dict}
        )
        if result.modified_count:
            updated_alarm = await self.alarms_collection.find_one({"_id": ObjectId(alarm_id)})
            return await self.data_adapter.convert_from_storage_format(updated_alarm)
        return None

    async def delete_alarm(self, alarm_id: str) -> bool:
        try:
            result = await self.alarms_collection.delete_one({"_id": ObjectId(alarm_id)})
            return result.deleted_count > 0
        except:
            return False

    async def acknowledge_alarm(self, alarm_id: str) -> bool:
        try:
            result = await self.alarms_collection.update_one(
                {"_id": ObjectId(alarm_id)},
                {"$set": {"acknowledged": True}}
            )
            return result.modified_count > 0
        except:
            return False

    async def create_user(self, user: UserCreate) -> UserResponse:
        user_dict = await self.data_adapter.convert_to_storage_format(user)
        result = await self.users_collection.insert_one(user_dict)
        created_user = await self.users_collection.find_one({"_id": result.inserted_id})
        return await self.data_adapter.convert_from_storage_format(created_user)

    async def get_user(self, user_id: str) -> Optional[UserResponse]:
        try:
            user = await self.users_collection.find_one({"_id": ObjectId(user_id)})
            if user:
                return await self.data_adapter.convert_from_storage_format(user)
            return None
        except:
            return None

    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        try:
            user = await self.users_collection.find_one({"email": email})
            if user:
                return await self.data_adapter.convert_from_storage_format(user)
            return None
        except:
            return None

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        cursor = self.users_collection.find().skip(skip).limit(limit)
        users = []
        async for user in cursor:
            converted_user = await self.data_adapter.convert_from_storage_format(user)
            users.append(converted_user)
        return users
