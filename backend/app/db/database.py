# statement for insert/update/delete 
# query for select

import asyncio

from sqlalchemy import String, text, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from models.database_model import Users, Students, Teachers


from db.config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True
)


async_session_factory = async_sessionmaker(engine)
# async_session = async_sessionmaker(engine)


async def select_data():
    async with async_session_factory as async_session:
        # Если хотим получить 1 сущность
        # student = await async_session.get(Students, {"id": 1})
        # return student
        query = await select(Teachers)
        result = await async_session.execute(query)
        teachers = result.scalars().all()
        print(teachers)

asyncio.run(select_data())