from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from config.config import Config
from src.repo import DB


class GetConfigMiddleware(BaseMiddleware):
    def __init__(self, config: Config):
        super().__init__()
        self.config = config

    async def __call__(
            self,
            handler: Callable[
                [TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        data["config"] = self.config

        return await handler(event, data)
