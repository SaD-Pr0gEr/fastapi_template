from fastapi import FastAPI

from core.config import Config
from db.postgres.db_async import AsyncPostgresEngine


class App(FastAPI):
    def __init__(
        self,
        config_: Config,
        async_pg_engine: AsyncPostgresEngine,
    ):
        super().__init__(title=config_.app.APP_NAME, debug=config_.server.DEBUG)
        self.config = config_
        self.db_async = async_pg_engine
