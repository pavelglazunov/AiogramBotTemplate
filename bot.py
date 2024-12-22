import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.config import load_config
from src.handlers import routers
from src.middlewares import (
    DbSessionMiddleware,
    MessageInPrivateMiddleware,
    GetConfigMiddleware,
)
from src.models import Base
from src.services import backups

logger = logging.getLogger(__name__)


async def main():
    load_dotenv()
    config = load_config()
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Start bot")

    engine = create_async_engine(url=config.db.url, echo=False)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    bot: Bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode='HTML'),
    )

    dp: Dispatcher = Dispatcher()

    dp.include_routers(*routers)

    dp.message.outer_middleware(MessageInPrivateMiddleware())

    dp.update.middleware(DbSessionMiddleware(sessionmaker))
    dp.update.middleware(GetConfigMiddleware(config))

    asyncio.create_task(backups.run(bot, config))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped')
