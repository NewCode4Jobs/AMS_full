# backend/app/repositories/base.py
from abc import ABC, abstractmethod
from typing import List, Optional
from ..schemas.alarm import AlarmCreate, AlarmResponse
from ..schemas.user import UserCreate, UserResponse

class BaseRepository(ABC):
    """Base repository interface defining operations for both alarms and users."""
    
    # Alarm operations
    @abstractmethod
    async def create_alarm(self, alarm: AlarmCreate) -> AlarmResponse:
        """Create a new alarm."""
        pass

    @abstractmethod
    async def get_alarm(self, alarm_id: int) -> Optional[AlarmResponse]:
        """Get an alarm by ID."""
        pass

    @abstractmethod
    async def get_all_alarms(self, skip: int = 0, limit: int = 100) -> List[AlarmResponse]:
        """Get all alarms with pagination."""
        pass

    @abstractmethod
    async def update_alarm(self, alarm_id: int, alarm: AlarmCreate) -> Optional[AlarmResponse]:
        """Update an existing alarm."""
        pass

    @abstractmethod
    async def delete_alarm(self, alarm_id: int) -> bool:
        """Delete an alarm."""
        pass

    @abstractmethod
    async def acknowledge_alarm(self, alarm_id: int) -> bool:
        """Acknowledge an alarm."""
        pass

    # User operations
    @abstractmethod
    async def create_user(self, user: UserCreate) -> UserResponse:
        """Create a new user."""
        pass

    @abstractmethod
    async def get_user(self, user_id: int) -> Optional[UserResponse]:
        """Get a user by ID."""
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Get a user by email."""
        pass

    @abstractmethod
    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Get all users with pagination."""
        pass
