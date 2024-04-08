# statement for insert/update/delete 
# query for select

import asyncio

from sqlalchemy import String, text, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase



from db.config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True
)


async_session_factory = async_sessionmaker(engine)
# async_session = async_sessionmaker(engine)
