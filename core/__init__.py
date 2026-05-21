from pathlib import Path

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from core.abstract import App
from core.apps import register_app_routes
from core.config import load_config
from core.middleware.request_id import request_identify_middleware
from core.settings.server import Config, Misc
from db.engine.postgres.db_async import AsyncPostgresEngine
from utils.logs import setup_logging


def make_app(
    toml_conf_path: str | Path,
    psql_env_path: str | Path,
    redis_env_path: str | Path,
    main_env_path: str | Path,
    misc: Misc,
) -> App:
    app_config = load_config(
        toml_conf_path, psql_env_path, redis_env_path, main_env_path, misc
    )
    setup_logging(app_config.server.LOGLEVEL.upper())
    main_db_async = AsyncPostgresEngine(
        app_config.main_db, echo=app_config.server.DEBUG
    )
    app = App(app_config, main_db_async)
    app.add_middleware(
        BaseHTTPMiddleware, dispatch=request_identify_middleware
    )
    app.add_middleware(
        TrustedHostMiddleware, allowed_hosts=app.config.app.ALLOWED_HOSTS
    )
    register_app_routes(app)
    return app
