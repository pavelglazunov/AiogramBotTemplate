from sqlalchemy.ext.asyncio import AsyncSession


class DB:
    def __init__(self, session: AsyncSession):
        ...
