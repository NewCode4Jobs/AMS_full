from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .core.config import settings
from .database.connection import init_db, close_db_connections
from .adapters.data_adapter import get_db_adapter, DatabaseAdapter
from .api.endpoints import alarms
from .models import alarm as alarm_model, user as user_model
from .schemas import alarm as alarm_schema, user as user_schema

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db_connections()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get repository
async def get_repository():
    db_adapter = get_db_adapter()
    async with db_adapter.get_repository() as repo:
        yield repo

# Include routers
app.include_router(
    alarms.router,
    prefix=settings.API_V1_STR,
    dependencies=[Depends(get_repository)]
)

# User endpoints
@app.post("/api/v1/users/", response_model=user_schema.UserResponse)
async def create_user(
    user: user_schema.UserCreate,
    repo=Depends(get_repository)
):
    return await repo.create_user(user)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Alarm Management System API",
        "docs_url": "/docs",
        "version": "1.0.0",
        "database": settings.DB_TYPE
    }