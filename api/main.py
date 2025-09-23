"""
AgenticAI Lab API Main Application

FastAPI application entry point with all routes, middleware, and configuration.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from contextlib import asynccontextmanager
import os
from typing import AsyncGenerator

from config import get_settings
from middleware import (
    LoggingMiddleware,
    RateLimitMiddleware,
    AuthenticationMiddleware
)
from routers import (
    auth,
    jobs,
    agents,
    webhooks,
    admin
)
from db.database import init_db, close_db


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.
    
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting AgenticAI Lab API...")
    
    # Initialize database
    await init_db()
    logger.info("Database initialized")
    
    # Initialize other services here
    # - Redis connection
    # - Message queue connections
    # - AI model loading
    
    yield
    
    # Shutdown
    logger.info("Shutting down AgenticAI Lab API...")
    
    # Close database connections
    await close_db()
    logger.info("Database connections closed")


# Create FastAPI application
app = FastAPI(
    title="AgenticAI Lab API",
    description="AI-Powered Content Creation Platform API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Get settings
settings = get_settings()

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(AuthenticationMiddleware)


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "type": "http_error"
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": 500,
                "message": "Internal server error",
                "type": "internal_error"
            }
        }
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "timestamp": "2025-01-01T00:00:00Z"
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to AgenticAI Lab API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health"
    }


# Include routers
app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["authentication"]
)

app.include_router(
    jobs.router,
    prefix="/api/v1/jobs",
    tags=["jobs"]
)

app.include_router(
    agents.router,
    prefix="/api/v1/agents",
    tags=["agents"]
)

app.include_router(
    webhooks.router,
    prefix="/api/v1/webhooks",
    tags=["webhooks"]
)

app.include_router(
    admin.router,
    prefix="/api/v1/admin",
    tags=["admin"]
)


def start():
    """Start the API server."""
    uvicorn.run(
        "api.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
        workers=settings.API_WORKERS if not settings.API_RELOAD else 1,
        log_level=settings.LOG_LEVEL.lower()
    )


if __name__ == "__main__":
    start()
