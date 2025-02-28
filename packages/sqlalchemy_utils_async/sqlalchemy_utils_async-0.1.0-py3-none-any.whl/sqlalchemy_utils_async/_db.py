from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text
from sqlalchemy.engine import URL, create_engine
import pathlib
from enum import Enum



class BaseDbUtil:
    def __init__(self, async_engine, bare_async_engine):
        self.async_engine = async_engine
        self.bare_async_engine = bare_async_engine

    async def check_exists(self):
        raise NotImplementedError


class PostgresqlDbUtil(BaseDbUtil):
    async def check_exists(self, dbname=None):
        dbname = dbname if dbname else self.async_engine.sync_engine.url.database
        exists = False
        async with self.bare_async_engine.connect() as conn:
            result = await (await conn.execution_options(
                stream_results=True
            )).stream(
                text("select datname from pg_database;")
            )
            async for row in result:
                # logger.info(row)
                if row[0] == dbname:
                    exists = True
        return exists


class SqliteDbUtil(BaseDbUtil):
    async def check_exists(self, dbname=None):
        db_path = pathlib.Path(self.async_engine.url.database)
        return db_path.is_file()


class MysqlDbUtil(BaseDbUtil):
    async def check_exists(self, dbname=None):
        dbname = dbname if dbname else self.async_engine.sync_engine.url.database
        exists = False
        async with self.bare_async_engine.connect() as conn:
            result = await (await conn.execution_options(
                stream_results=True
            )).stream(
                text("show databases;")
            )
            async for row in result:
                # logger.info(row)
                if row[0] == dbname:
                    exists = True
        return exists


class DbBackend(Enum):
    sqlite = SqliteDbUtil
    postgresql = PostgresqlDbUtil
    mysql = MysqlDbUtil


class UnionDbUtil:

    db_backend: str
    backend_util: BaseDbUtil

    def __init__(self, async_engine: AsyncEngine):
        self.async_engine = async_engine
        sync_engine = async_engine.sync_engine
        url = sync_engine.url
        bare_url = URL.create(
            drivername=url.drivername,
            username=url.username,
            password=url.password,
            host=url.host,
            port=url.port,
        )
        self.bare_async_engine = AsyncEngine(
            sync_engine=create_engine(
                url=bare_url
            )
        )

    def guess_db_backend(self) -> BaseDbUtil:
        if self.async_engine.url.drivername.startswith('sqlite'):
            self.db_backend = DbBackend.sqlite.name
        elif self.async_engine.url.drivername.startswith('postgresql'):
            self.db_backend = DbBackend.postgresql.name
        elif self.async_engine.url.drivername.startswith('mysql'):
            self.db_backend = DbBackend.mysql.name
        else:
            raise NotImplementedError

        self.backend_util = getattr(
            DbBackend, self.db_backend
        ).value(
            async_engine=self.async_engine,
            bare_async_engine=self.bare_async_engine,
        )
        return self.backend_util


