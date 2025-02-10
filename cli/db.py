import click
import sqlalchemy as sa
from dotenv import load_dotenv
from sqlalchemy import create_engine

from core.config import Misc
from core.settings.db import PostgresConfig
from db.postgres.db_sync import SyncPgEngine

load_dotenv('../.envs/psql.env')

@click.command("test-connection", help="Test Db connection")
def test_connection():
    misc = Misc()
    engine = SyncPgEngine(create_engine(
        PostgresConfig(_env_file=misc.PSQL_ENV, _case_sensitive=False).db_url
    ))
    with engine.session_class() as session:
        session.execute(sa.text("SELECT 1;"))
    print("CONNECTION IS STABLE!")
