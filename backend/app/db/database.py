# statement for insert/update/delete 
# query for select
from typing import AsyncGenerator

from sqlalchemy import String, text, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase

from models.database_model import User



from db.config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True
)


async_session_factory = async_sessionmaker(engine)


# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)