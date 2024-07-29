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
class Config:
    bot: Bot
    db: Db


def load_config() -> Config:
    load_dotenv()
    return Config(
        bot=Bot(
            token=getenv("TOKEN"),
        ),
        db=Db(
            url=getenv("DB_URL"),
        ),
    )


config: Config = load_config()
