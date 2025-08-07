import logging
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from redis.asyncio import Redis

BASE_DIR = Path(__file__).resolve().parent.parent

DEFAULT_LOG_FORMAT = (
    "[%(asctime)s] %(module)15s:%(lineno)-3d %(levelname)8s - %(message)s"
)

WORKER_DEFAULT_LOG_FORMAT = (
    "[%(asctime)s] [%(processName)s] %(module)15s:%(lineno)-3d %(levelname)8s - %(message)s"
)


class GunicornConfig(BaseModel):
    host: str
    port: int
    workers: int
    timeout: int


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    logging.Formatter.default_msec_format = '%s.%03d'
    log_format: str = DEFAULT_LOG_FORMAT

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class TaskiqConfig(BaseModel):
    url: str
    log_format: str = WORKER_DEFAULT_LOG_FORMAT


class MailingConfig(BaseModel):
    host: str
    port: int
    sender: str = "fastapi-journal@example.com"


class RedisConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    user_password: str
    db: int


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class AuthJWTConfig(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"
    access_token_ttl: int = 60 * 60  # 1 hour
    refresh_token_ttl: int = 60 * 60 * 24 * 30  # 30 days(≈1 month)

    @property
    def private_key(self):
        return self.private_key_path.read_text()

    @property
    def public_key(self):
        return self.public_key_path.read_text()


class AuthConfig(BaseModel):
    session_ttl: int = 60 * 60 * 24 * 7  # 1 week (7 days)
    secret_key: bytes


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="ignore",
    )
    gunicorn: GunicornConfig
    logging: LoggingConfig = LoggingConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    taskiq: TaskiqConfig
    mailing: MailingConfig
    redis: RedisConfig
    auth: AuthConfig


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()

redis_client = Redis(
    host=settings.redis.host,
    port=settings.redis.port,
    username=settings.redis.username,
    password=settings.redis.user_password,
    db=settings.redis.db,
)
