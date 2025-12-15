from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from .env file"""
    
    PROJECT_NAME: str = "FastAPI Server"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./app.db"
    DEBUG: bool = False
    
    # JWT Settings
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
