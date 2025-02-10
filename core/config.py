import tomllib
from pathlib import Path

from core.settings.db import PostgresConfig, RedisConfig
from core.settings.server import AppConfig, Config, Misc, ServerConfig, UrlNames


def load_config(
    config_toml_path: str | Path,
    psql_env_path: str | Path,
    redis_env_path: str | Path,
    others_env_path: str | Path,
    misc: Misc | None = None,
) -> Config:
    with open(config_toml_path, "rb") as file:
        config = tomllib.load(file)
    if not misc:
        misc = Misc()
    app_config = AppConfig(**config["app"])
    server_config = ServerConfig(**config["server"])
    pg_db_config = PostgresConfig(
        _env_file=psql_env_path,  # type: ignore
        _case_sensitive=False,  # type: ignore
    )
    redis_conf = RedisConfig(
        _env_file=redis_env_path,  # type: ignore
        _case_sensitive=False,  # type: ignore
    )
    return Config(
        _env_file=others_env_path,  # type: ignore
        _case_sensitive=False,  # type: ignore
        app=app_config,
        server=server_config,
        main_db=pg_db_config,
        cache_db=redis_conf,
        misc=misc,
        urls=UrlNames(),
    )
