from dataclasses import dataclass
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings

from . import db as db_conf


class ServerConfig(BaseSettings):
    HOST: str = Field(default="127.0.0.1")
    PORT: int = Field(default=8000)
    DEBUG: bool = Field(default=True)
    LOGLEVEL: str = Field(default="DEBUG")


class AppConfig(BaseSettings):
    APP_NAME: str
    ALLOWED_HOSTS: list[str] = Field(default=["127.0.0.1"])


class UrlNames(BaseSettings):
    CORE_GET: str = "core_get"


@dataclass
class Misc:
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    APP_DIR: Path = BASE_DIR / "core"
    MAIN_ENV: Path = BASE_DIR / ".envs/.env"
    PSQL_ENV: Path = BASE_DIR / ".envs/psql.env"
    REDIS_ENV: Path = BASE_DIR / ".envs/redis.env"
    TOML_CONFIG: Path = BASE_DIR / "config.toml"


class Config(BaseSettings):
    server: ServerConfig
    app: AppConfig
    main_db: db_conf.PostgresConfig
    cache_db: db_conf.RedisConfig
    misc: Misc
    urls: UrlNames
