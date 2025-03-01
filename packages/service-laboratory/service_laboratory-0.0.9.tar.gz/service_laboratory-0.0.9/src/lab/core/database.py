from alembic import command
from alembic.config import Config
from litestar.plugins.sqlalchemy import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyPlugin,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ..settings import settings

session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=settings.database_uri,
    before_send_handler="autocommit",
    session_config=session_config,
)
alchemy = SQLAlchemyPlugin(config=sqlalchemy_config)

engine = create_async_engine(settings.database_uri, echo=False)
session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


def run_migrations(script_location):
    def ___execute__(connection):
        cfg = Config()
        cfg.set_main_option("script_location", script_location)
        cfg.attributes["connection"] = connection
        command.upgrade(cfg, "head")

    return ___execute__
