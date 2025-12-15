from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from .env file"""
    
    PROJECT_NAME: str = "FastAPI Server"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./app.db"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
