from os import PathLike

from starlette.middleware.trustedhost import TrustedHostMiddleware

from core.abstract import App
from core.apps import register_app_routes
from core.config import load_config
from core.settings.server import Config, Misc
from db.postgres.db_async import AsyncPostgresEngine


def make_app(
    toml_conf_path: str | PathLike, psql_env_path: str | PathLike,
    redis_env_path: str | PathLike, main_env_path: str | PathLike, misc: Misc
) -> App:
    app_config = load_config(
        toml_conf_path, psql_env_path, redis_env_path, main_env_path, misc
    )
    main_db_async = AsyncPostgresEngine(
        app_config.main_db, echo=app_config.server.DEBUG
    )
    app = App(app_config, main_db_async)
    app.add_middleware(
        TrustedHostMiddleware, allowed_hosts=app.config.app.ALLOWED_HOSTS
    )
    register_app_routes(app)
    return app
