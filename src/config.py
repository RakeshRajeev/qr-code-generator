import os
from dotenv import load_dotenv
from functools import lru_cache
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # Required settings
    database_url: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/qr_code_db")
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", 6379))
    celery_broker_url: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    
    # Optional settings
    db_password: str | None = os.getenv("DB_PASSWORD")
    docker_username: str | None = os.getenv("DOCKER_USERNAME")
    tag: str | None = os.getenv("TAG")
    restart_policy: str | None = os.getenv("RESTART_POLICY")
    dev_code_mount: str | None = os.getenv("DEV_CODE_MOUNT")
    dev_reload: str | None = os.getenv("DEV_RELOAD")

    model_config = ConfigDict(
        env_file=".env",
        extra="allow",  # Allow extra fields
        protected_namespaces=()
    )

@lru_cache()
def get_settings():
    return Settings()
