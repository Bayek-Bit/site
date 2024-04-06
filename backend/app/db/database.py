# statement for insert/update/delete 
# query for select
from sqlalchemy import String, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from models.database_model import Users


from config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True
)


async_session_factory = async_sessionmaker(engine)
# async_session = async_sessionmaker(engine)


async def insert_data():
    async with async_session_factory as async_session:
        user_1 = Users(username="User_1", password="12323")
        user_2 = Users(username="User_2", password="1323323")
        # запрос ещё не был отправлен, поэтому await не нужен.
        async_session.add_all([user_1, user_2])
        await async_session.commit()