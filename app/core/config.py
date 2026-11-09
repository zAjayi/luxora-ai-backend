from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "LuxoraAI"
    DATABASE_URL: str = "postgresql://user:password@localhost/luxoraai?sslmode=require"
    OPENROUTER_API_KEY: str = ""
    JWT_SECRET_KEY: str | None = None
    SENTRY_DSN: str | None = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    STRIPE_SECRET_KEY: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
