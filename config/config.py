import logging
from dataclasses import dataclass

from dotenv import load_dotenv

from .base import getenv


# logging
def init_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("app.log")


@dataclass
class Bot:
    token: str


@dataclass
class Db:
    url: str


@dataclass
class Channels:
    backup: int


@dataclass
class Config:
    bot: Bot
    db: Db
    channels: Channels


def load_config() -> Config:
    load_dotenv()
    return Config(
        bot=Bot(
            token=getenv("TOKEN"),
        ),
        db=Db(
            url=getenv("DB_URL"),
        ),
        channels=Channels(
            backup=int(getenv("CHANNEL_BACKUP")),
        ),
    )
