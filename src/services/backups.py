import asyncio

from aiogram import Bot, types
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from config.config import Config


async def do_backup(bot: Bot, config: Config):
    while True:
        try:
            await asyncio.sleep(86400 // 4)

            await bot.send_document(
                chat_id=config.channels.backup,
                document=types.FSInputFile('main.db'),
            )
        except (TelegramBadRequest, TelegramForbiddenError):
            await asyncio.sleep(20 * 60)
