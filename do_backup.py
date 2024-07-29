import asyncio

from aiogram import Bot, types

from config.config import config


async def do_backup(bot: Bot):

    while True:
        await asyncio.sleep(86400 // 4)

        await bot.send_document(
            chat_id=config.channels.backup,
            document=types.FSInputFile('main.db'),
        )

