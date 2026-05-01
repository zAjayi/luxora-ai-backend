import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "LuxoraAI"
    DATABASE_URL: str = "postgresql://user:password@localhost/luxoraai"
    OPENROUTER_API_KEY: str = ""
    JWT_SECRET_KEY: str | None = None
    STRIPE_SECRET_KEY: str | None = None
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
