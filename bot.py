import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import do_backup
from config.config import config
from do_backup import do_backup
from src.handlers import routers
from src.middlewares import DbSessionMiddleware, GetUserMiddleware, IsBlockedMiddleware, \
    MessageInPrivateMiddleware, MessageInSSKMiddleware
from src.models import Base
from src.services import pairs, load_admins, survey, feedback

logger = logging.getLogger(__name__)


async def main():
    load_dotenv()
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Start bot")

    engine = create_async_engine(url=config.db.url, echo=False)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    # TODO миграций нет - мб стоит их добавить
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

    dp.message.outer_middleware(GetUserMiddleware())
    dp.callback_query.outer_middleware(GetUserMiddleware())

    dp.message.outer_middleware(MessageInSSKMiddleware())
    dp.callback_query.outer_middleware(MessageInSSKMiddleware())

    dp.message.outer_middleware(IsBlockedMiddleware())
    dp.callback_query.outer_middleware(IsBlockedMiddleware())

    asyncio.create_task(do_backup(bot))
    asyncio.create_task(feedback.run(bot, sessionmaker))
    asyncio.create_task(survey.run(bot, sessionmaker))
    asyncio.create_task(pairs.run(bot, sessionmaker))

    await load_admins.load(sessionmaker)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped')
