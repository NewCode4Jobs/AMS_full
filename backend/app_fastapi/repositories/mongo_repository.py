from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from ..schemas import AlarmCreate, AlarmResponse, UserCreate, UserResponse
from .base import BaseRepository

class MongoRepository(BaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.alarms_collection = db.alarms
        self.users_collection = db.users

    async def create_alarm(self, alarm: AlarmCreate) -> AlarmResponse:
        alarm_dict = alarm.dict()
        alarm_dict["timestamp"] = datetime.utcnow()
        result = await self.alarms_collection.insert_one(alarm_dict)
        created_alarm = await self.alarms_collection.find_one({"_id": result.inserted_id})
        created_alarm["id"] = str(created_alarm.pop("_id"))
        return AlarmResponse(**created_alarm)

    async def get_alarm(self, alarm_id: int) -> Optional[AlarmResponse]:
        alarm = await self.alarms_collection.find_one({"_id": ObjectId(str(alarm_id))})
        if alarm:
            alarm["id"] = str(alarm.pop("_id"))
            return AlarmResponse(**alarm)
        return None

    async def get_all_alarms(self, skip: int = 0, limit: int = 100) -> List[AlarmResponse]:
        cursor = self.alarms_collection.find().skip(skip).limit(limit)
        alarms = []
        async for alarm in cursor:
            alarm["id"] = str(alarm.pop("_id"))
            alarms.append(AlarmResponse(**alarm))
        return alarms

    async def update_alarm(self, alarm_id: int, alarm: AlarmCreate) -> Optional[AlarmResponse]:
        alarm_dict = alarm.dict()
        result = await self.alarms_collection.update_one(
            {"_id": ObjectId(str(alarm_id))},
            {"$set": alarm_dict}
        )
        if result.modified_count:
            updated_alarm = await self.alarms_collection.find_one({"_id": ObjectId(str(alarm_id))})
            updated_alarm["id"] = str(updated_alarm.pop("_id"))
            return AlarmResponse(**updated_alarm)
        return None

    async def delete_alarm(self, alarm_id: int) -> bool:
        result = await self.alarms_collection.delete_one({"_id": ObjectId(str(alarm_id))})
        return result.deleted_count > 0

    async def acknowledge_alarm(self, alarm_id: int) -> bool:
        result = await self.alarms_collection.update_one(
            {"_id": ObjectId(str(alarm_id))},
            {"$set": {"acknowledged": True}}
        )
        return result.modified_count > 0

    async def create_user(self, user: UserCreate) -> UserResponse:
        user_dict = user.dict()
        user_dict["is_active"] = True
        # TODO: Hash password
        result = await self.users_collection.insert_one(user_dict)
        created_user = await self.users_collection.find_one({"_id": result.inserted_id})
        created_user["id"] = str(created_user.pop("_id"))
        return UserResponse(**created_user)

    async def get_user(self, user_id: int) -> Optional[UserResponse]:
        user = await self.users_collection.find_one({"_id": ObjectId(str(user_id))})
        if user:
            user["id"] = str(user.pop("_id"))
            return UserResponse(**user)
        return None

    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        user = await self.users_collection.find_one({"email": email})
        if user:
            user["id"] = str(user.pop("_id"))
            return UserResponse(**user)
        return None

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        cursor = self.users_collection.find().skip(skip).limit(limit)
        users = []
        async for user in cursor:
            user["id"] = str(user.pop("_id"))
            users.append(UserResponse(**user))
        return users
