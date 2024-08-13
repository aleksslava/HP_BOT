import asyncio
# from sqlalchemy import text
# from sqlalchemy.dialects.postgresql import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from config_data.config import load_db_settings
from sqlalchemy.orm import DeclarativeBase


# async_engine = create_async_engine(
#     url=load_db_settings().database_url_asyncpg,
#     echo=True,
# )


class Base(DeclarativeBase):
    pass


class Database:

    @staticmethod
    def is_admin(list_admin: list[int], user_id: int) -> bool:
        return user_id in list_admin


