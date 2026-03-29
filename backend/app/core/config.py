from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str = "postgresql://mindmirror:mindmirror@localhost:5432/mindmirror"
    admin_password: str = "change-me-in-production"
    jwt_secret: str = "change-me-to-a-random-string"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"
    cors_origins: str = "http://localhost:3000"
    automation_secret: str = "change-me-webhook-secret"
    app_env: str = "development"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
