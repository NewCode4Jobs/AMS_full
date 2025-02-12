from typing import Optional, List, Protocol
from abc import ABC, abstractmethod
from ..schemas.alarm import AlarmCreate, AlarmResponse
from ..schemas.user import UserCreate, UserResponse


class RepositoryError(Exception):
    """Base exception for repository errors."""
    pass


class NotFoundError(RepositoryError):
    """Raised when an entity is not found."""
    pass


class DuplicateError(RepositoryError):
    """Raised when attempting to create a duplicate entity."""
    pass


class AlarmRepository(Protocol):
    """
    Protocol defining the interface for alarm operations.
    Concrete implementations should implement this protocol for alarm-related operations.
    """
    
    async def create_alarm(self, alarm: AlarmCreate) -> AlarmResponse:
        """Create a new alarm."""
        ...
    
    async def get_alarm(self, alarm_id: str) -> Optional[AlarmResponse]:
        """Get an alarm by ID."""
        ...
    
    async def get_all_alarms(self, skip: int = 0, limit: int = 100) -> List[AlarmResponse]:
        """Get all alarms with pagination."""
        ...
    
    async def update_alarm(self, alarm_id: str, alarm: AlarmCreate) -> Optional[AlarmResponse]:
        """Update an alarm by ID."""
        ...
    
    async def delete_alarm(self, alarm_id: str) -> bool:
        """Delete an alarm by ID."""
        ...
    
    async def acknowledge_alarm(self, alarm_id: str) -> bool:
        """Acknowledge an alarm."""
        ...


class UserRepository(Protocol):
    """
    Protocol defining the interface for user operations.
    Concrete implementations should implement this protocol for user-related operations.
    """
    
    async def create_user(self, user: UserCreate) -> UserResponse:
        """Create a new user."""
        ...
    
    async def get_user(self, user_id: str) -> Optional[UserResponse]:
        """Get a user by ID."""
        ...
    
    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Get a user by email."""
        ...
    
    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Get all users with pagination."""
        ...


class BaseAlarmRepository:
    """
    Base implementation for alarm repositories with common helper methods.
    Concrete implementations can inherit from this class to get the helper methods.
    """
    
    async def get_alarm_or_404(self, alarm_id: str) -> AlarmResponse:
        """Get an alarm by ID or raise NotFoundError."""
        if not hasattr(self, 'get_alarm'):
            raise NotImplementedError("get_alarm method not implemented")
            
        alarm = await self.get_alarm(alarm_id)
        if alarm is None:
            raise NotFoundError(f"Alarm with id {alarm_id} not found")
        return alarm
    
    async def update_alarm_or_404(self, alarm_id: str, alarm: AlarmCreate) -> AlarmResponse:
        """Update an alarm by ID or raise NotFoundError."""
        if not hasattr(self, 'update_alarm'):
            raise NotImplementedError("update_alarm method not implemented")
            
        updated = await self.update_alarm(alarm_id, alarm)
        if updated is None:
            raise NotFoundError(f"Alarm with id {alarm_id} not found")
        return updated
    
    async def delete_alarm_or_404(self, alarm_id: str) -> bool:
        """Delete an alarm by ID or raise NotFoundError."""
        if not hasattr(self, 'get_alarm') or not hasattr(self, 'delete_alarm'):
            raise NotImplementedError("get_alarm or delete_alarm method not implemented")
            
        alarm = await self.get_alarm(alarm_id)
        if alarm is None:
            raise NotFoundError(f"Alarm with id {alarm_id} not found")
        return await self.delete_alarm(alarm_id)


class BaseUserRepository:
    """
    Base implementation for user repositories with common helper methods.
    Concrete implementations can inherit from this class to get the helper methods.
    """
    
    async def get_user_or_404(self, user_id: str) -> UserResponse:
        """Get a user by ID or raise NotFoundError."""
        if not hasattr(self, 'get_user'):
            raise NotImplementedError("get_user method not implemented")
            
        user = await self.get_user(user_id)
        if user is None:
            raise NotFoundError(f"User with id {user_id} not found")
        return user
