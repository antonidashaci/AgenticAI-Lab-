"""
Middleware Components

Custom middleware for the FastAPI application.
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging
from typing import Callable
import redis
import json
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP requests and responses.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.url}")
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response
        logger.info(
            f"Response: {response.status_code} - "
            f"Processing time: {process_time:.4f}s"
        )
        
        # Add processing time header
        response.headers["X-Process-Time"] = str(process_time)
        
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware for rate limiting requests.
    """
    
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.redis_client = None
        
        # Try to connect to Redis
        try:
            self.redis_client = redis.from_url(settings.REDIS_URL)
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}. Rate limiting disabled.")
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not self.redis_client:
            # If Redis is not available, skip rate limiting
            return await call_next(request)
        
        # Get client IP
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        
        try:
            # Get current request count
            current_requests = self.redis_client.get(key)
            
            if current_requests is None:
                # First request from this IP
                self.redis_client.setex(key, 60, 1)  # Expire in 60 seconds
            else:
                current_count = int(current_requests)
                if current_count >= self.requests_per_minute:
                    # Rate limit exceeded
                    return Response(
                        content=json.dumps({
                            "error": {
                                "code": 429,
                                "message": "Rate limit exceeded",
                                "type": "rate_limit_error"
                            }
                        }),
                        status_code=429,
                        media_type="application/json"
                    )
                else:
                    # Increment counter
                    self.redis_client.incr(key)
            
        except Exception as e:
            logger.warning(f"Rate limiting error: {e}")
            # Continue without rate limiting if Redis fails
        
        return await call_next(request)


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """
    Middleware for handling authentication.
    """
    
    # Public paths that don't require authentication
    PUBLIC_PATHS = {
        "/",
        "/health",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/api/v1/auth/login",
        "/api/v1/auth/register",
        "/api/v1/auth/refresh"
    }
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        path = request.url.path
        
        # Skip authentication for public paths
        if path in self.PUBLIC_PATHS or path.startswith("/static/"):
            return await call_next(request)
        
        # For now, we'll skip authentication implementation
        # TODO: Implement JWT token validation
        
        return await call_next(request)
