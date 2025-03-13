import os
from dotenv import load_dotenv
from functools import lru_cache
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL")
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", 6379))
    celery_broker_url: str = os.getenv("CELERY_BROKER_URL")

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
