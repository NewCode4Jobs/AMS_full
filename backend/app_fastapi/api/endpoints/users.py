from fastapi import APIRouter, Depends
from ...schemas import user as user_schema
from ...dependencies import get_repository

router = APIRouter()

@router.post("/users/", response_model=user_schema.UserResponse)
async def create_user(
    user: user_schema.UserCreate,
    repo=Depends(get_repository)
):
    """
    Create a new user in the system.
    
    Args:
        user (UserCreate): User creation details
        repo: Repository dependency for user operations
    
    Returns:
        UserResponse: Created user details
    """
    return await repo.create_user(user)
