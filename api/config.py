"""
Configuration Management

Centralized configuration using Pydantic Settings.
"""

try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings
from pydantic import Field, validator
from typing import List, Optional
import os
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""
    
    # Environment
    NODE_ENV: str = Field(default="development")
    PYTHON_ENV: str = Field(default="development")
    DEBUG: bool = Field(default=True)
    LOG_LEVEL: str = Field(default="DEBUG")
    
    # API Configuration
    API_HOST: str = Field(default="localhost")
    API_PORT: int = Field(default=8000)
    API_WORKERS: int = Field(default=1)
    API_RELOAD: bool = Field(default=True)
    
    # Database Configuration
    DATABASE_URL: str = Field(
        default="postgresql://agenticai_user:agenticai_password@localhost:5432/agenticai_dev"
    )
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_DB: str = Field(default="agenticai_dev")
    POSTGRES_USER: str = Field(default="agenticai_user")
    POSTGRES_PASSWORD: str = Field(default="agenticai_password")
    
    # Redis Configuration
    REDIS_URL: str = Field(default="redis://:agenticai_redis_password@localhost:6379/0")
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_PASSWORD: str = Field(default="agenticai_redis_password")
    REDIS_DB: int = Field(default=0)
    
    # Qdrant Configuration
    QDRANT_URL: str = Field(default="http://localhost:6333")
    QDRANT_HOST: str = Field(default="localhost")
    QDRANT_PORT: int = Field(default=6333)
    QDRANT_API_KEY: Optional[str] = Field(default=None)
    
    # RabbitMQ Configuration
    RABBITMQ_URL: str = Field(
        default="amqp://agenticai_user:agenticai_password@localhost:5672/agenticai"
    )
    RABBITMQ_HOST: str = Field(default="localhost")
    RABBITMQ_PORT: int = Field(default=5672)
    RABBITMQ_USER: str = Field(default="agenticai_user")
    RABBITMQ_PASSWORD: str = Field(default="agenticai_password")
    RABBITMQ_VHOST: str = Field(default="agenticai")
    
    # Temporal Configuration
    TEMPORAL_HOST: str = Field(default="localhost")
    TEMPORAL_PORT: int = Field(default=7233)
    TEMPORAL_NAMESPACE: str = Field(default="default")
    TEMPORAL_TASK_QUEUE: str = Field(default="agenticai-tasks")
    
    # AI Services Configuration
    OPENAI_API_KEY: Optional[str] = Field(default=None)
    OPENAI_ORG_ID: Optional[str] = Field(default=None)
    OPENAI_MODEL_DEFAULT: str = Field(default="gpt-4-turbo-preview")
    
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None)
    ANTHROPIC_MODEL_DEFAULT: str = Field(default="claude-3-sonnet-20240229")
    
    ELEVENLABS_API_KEY: Optional[str] = Field(default=None)
    ELEVENLABS_VOICE_ID: Optional[str] = Field(default=None)
    
    OLLAMA_BASE_URL: str = Field(default="http://localhost:11434")
    OLLAMA_MODEL_DEFAULT: str = Field(default="llama3.1:8b")
    
    # Supabase Configuration
    SUPABASE_URL: Optional[str] = Field(default=None)
    SUPABASE_ANON_KEY: Optional[str] = Field(default=None)
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = Field(default=None)
    
    # MinIO Configuration
    MINIO_ENDPOINT: str = Field(default="localhost:9000")
    MINIO_ACCESS_KEY: str = Field(default="agenticai_admin")
    MINIO_SECRET_KEY: str = Field(default="agenticai_password_123")
    MINIO_BUCKET: str = Field(default="agenticai-storage")
    MINIO_SECURE: bool = Field(default=False)
    
    # Authentication & Security
    JWT_SECRET_KEY: str = Field(default="your_super_secret_jwt_key_change_in_production")
    JWT_ALGORITHM: str = Field(default="HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=30)
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:3001", "http://localhost:3000"])
    CORS_CREDENTIALS: bool = Field(default=True)
    
    # Allowed hosts
    ALLOWED_HOSTS: List[str] = Field(default=["localhost", "127.0.0.1", "0.0.0.0"])
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = Field(default=100)
    RATE_LIMIT_WINDOW: int = Field(default=60)
    
    # File Storage
    STORAGE_PATH: str = Field(default="./storage")
    UPLOAD_PATH: str = Field(default="./storage/uploads")
    GENERATED_PATH: str = Field(default="./storage/generated")
    TEMP_PATH: str = Field(default="./storage/temp")
    ARCHIVE_PATH: str = Field(default="./storage/archive")
    
    # Model Storage
    MODELS_PATH: str = Field(default="./models")
    OLLAMA_MODELS_PATH: str = Field(default="./models/ollama")
    
    # Feature Flags
    ENABLE_REGISTRATION: bool = Field(default=True)
    ENABLE_AI_FEATURES: bool = Field(default=True)
    ENABLE_VIDEO_GENERATION: bool = Field(default=True)
    ENABLE_VOICE_CLONING: bool = Field(default=False)
    ENABLE_ANALYTICS: bool = Field(default=True)
    ENABLE_WEBHOOKS: bool = Field(default=True)
    ENABLE_API_ACCESS: bool = Field(default=True)
    
    # Performance Settings
    WORKER_CONCURRENCY: int = Field(default=4)
    CACHE_TTL: int = Field(default=3600)
    GPU_MEMORY_FRACTION: float = Field(default=0.8)
    
    @validator('CORS_ORIGINS', pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    @validator('ALLOWED_HOSTS', pre=True)
    def parse_allowed_hosts(cls, v):
        """Parse allowed hosts from string or list."""
        if isinstance(v, str):
            return [host.strip() for host in v.split(',')]
        return v
    
    class Config:
        env_file = ".env.local"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings instance
    """
    return Settings()
