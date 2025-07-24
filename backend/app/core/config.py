from typing import Any, Dict, List, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "PhD Progress Tracker"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    POSTGRES_SERVER: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "phd_tracker"
    DATABASE_URL: Optional[str] = None
    DATABASE_URL_SYNC: Optional[str] = None
    
    @field_validator("DATABASE_URL", mode="before")
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        server = values.data.get('POSTGRES_SERVER', 'postgres')
        user = values.data.get('POSTGRES_USER', 'postgres')
        password = values.data.get('POSTGRES_PASSWORD', 'postgres')
        db = values.data.get('POSTGRES_DB', 'phd_tracker')
        return f"postgresql+asyncpg://{user}:{password}@{server}/{db}"
    
    @field_validator("DATABASE_URL_SYNC", mode="before")
    def assemble_db_connection_sync(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        server = values.data.get('POSTGRES_SERVER', 'postgres')
        user = values.data.get('POSTGRES_USER', 'postgres')
        password = values.data.get('POSTGRES_PASSWORD', 'postgres')
        db = values.data.get('POSTGRES_DB', 'phd_tracker')
        return f"postgresql://{user}:{password}@{server}/{db}"
    
    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_URL: Optional[str] = None
    
    @field_validator("REDIS_URL", mode="before")
    def assemble_redis_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return f"redis://{values.data.get('REDIS_HOST')}:{values.data.get('REDIS_PORT')}"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000", "http://localhost:5173"]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Email
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None
    
    # First superuser
    FIRST_SUPERUSER: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "changethis"
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()