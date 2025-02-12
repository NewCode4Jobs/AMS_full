from typing import Generic, TypeVar, Optional, List, Any
from abc import ABC, abstractmethod
from pydantic import BaseModel
from ..schemas.alarm import AlarmCreate, AlarmResponse
from ..schemas.user import UserCreate, UserResponse

T = TypeVar('T', bound=BaseModel)


class RepositoryError(Exception):
    """Base exception for repository errors."""
    pass


class NotFoundError(RepositoryError):
    """Raised when an entity is not found."""
    pass


class DuplicateError(RepositoryError):
    """Raised when attempting to create a duplicate entity."""
    pass


class BaseRepository(ABC, Generic[T]):
    """
    Abstract base repository defining the interface for all repositories.
    Generic type T must be a Pydantic model.
    """
    
    @abstractmethod
    async def create(self, entity: T) -> T:
        """Create a new entity."""
        pass
    
    @abstractmethod
    async def get(self, id: Any) -> Optional[T]:
        """Get an entity by ID."""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all entities with pagination."""
        pass
    
    @abstractmethod
    async def update(self, id: Any, entity: T) -> Optional[T]:
        """Update an entity by ID."""
        pass
    
    @abstractmethod
    async def delete(self, id: Any) -> bool:
        """Delete an entity by ID."""
        pass
    
    @abstractmethod
    async def exists(self, id: Any) -> bool:
        """Check if an entity exists by ID."""
        pass
    
    async def get_or_404(self, id: Any) -> T:
        """Get an entity by ID or raise NotFoundError."""
        entity = await self.get(id)
        if entity is None:
            raise NotFoundError(f"Entity with id {id} not found")
        return entity
    
    async def update_or_404(self, id: Any, entity: T) -> T:
        """Update an entity by ID or raise NotFoundError."""
        updated = await self.update(id, entity)
        if updated is None:
            raise NotFoundError(f"Entity with id {id} not found")
        return updated
    
    async def delete_or_404(self, id: Any) -> bool:
        """Delete an entity by ID or raise NotFoundError."""
        if not await self.exists(id):
            raise NotFoundError(f"Entity with id {id} not found")
        return await self.delete(id)
    
    async def create_if_not_exists(self, entity: T) -> T:
        """Create an entity if it doesn't exist, otherwise return existing."""
        if hasattr(entity, 'id') and entity.id:
            existing = await self.get(entity.id)
            if existing:
                return existing
        return await self.create(entity)


class AlarmRepository(BaseRepository[AlarmResponse]):
    """Repository for alarm operations."""
    
    # Alarm operations
    async def create_alarm(self, alarm: AlarmCreate) -> AlarmResponse:
        """Create a new alarm."""
        return await self.create(alarm)
    
    async def get_alarm(self, alarm_id: int) -> Optional[AlarmResponse]:
        """Get an alarm by ID."""
        return await self.get(alarm_id)
    
    async def get_all_alarms(self, skip: int = 0, limit: int = 100) -> List[AlarmResponse]:
        """Get all alarms with pagination."""
        return await self.get_all(skip, limit)
    
    async def update_alarm(self, alarm_id: int, alarm: AlarmCreate) -> Optional[AlarmResponse]:
        """Update an existing alarm."""
        return await self.update(alarm_id, alarm)
    
    async def delete_alarm(self, alarm_id: int) -> bool:
        """Delete an alarm."""
        return await self.delete(alarm_id)
    
    async def acknowledge_alarm(self, alarm_id: int) -> bool:
        """Acknowledge an alarm."""
        # This method is not implemented in the base repository, 
        # you might want to add it or raise a NotImplementedError
        raise NotImplementedError


class UserRepository(BaseRepository[UserResponse]):
    """Repository for user operations."""
    
    # User operations
    async def create_user(self, user: UserCreate) -> UserResponse:
        """Create a new user."""
        return await self.create(user)
    
    async def get_user(self, user_id: int) -> Optional[UserResponse]:
        """Get a user by ID."""
        return await self.get(user_id)
    
    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Get a user by email."""
        # This method is not implemented in the base repository, 
        # you might want to add it or raise a NotImplementedError
        raise NotImplementedError
    
    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Get all users with pagination."""
        return await self.get_all(skip, limit)
