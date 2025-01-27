from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .core.config import settings
from .api.endpoints import alarms, users
from .database.connection import get_db
from .dependencies import get_repository

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    yield
    # Shutdown

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    alarms.router,
    prefix=settings.API_V1_STR,
    dependencies=[Depends(get_repository)]
)

app.include_router(
    users.router,
    prefix=settings.API_V1_STR,
    dependencies=[Depends(get_repository)]
)

@app.get("/")
def alive():
    return {
        "message": "Welcome to Alarm Management System API",
        "docs_url": "/docs",
        "database_used": settings.DB_TYPE
    }