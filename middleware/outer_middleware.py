from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

"""Функция для проброса в хэндел соединения с БД"""


class DBMiddleware(BaseMiddleware):

    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]) -> Any:
        # Тут будет создание соединения с бд и добавление его в словарь

        async with self.session() as conn:
            data['db'] = conn
            result = await handler(event, data)

        # Тут будет закрытие соединения с БД

        return result
