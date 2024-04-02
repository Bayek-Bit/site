import asyncio

from sqlalchemy import String, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from config import settings


engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True
)


async def get_all():
    async with engine.connect() as conn:
        res = await conn.execute(text("SELECT * from teachers"))
        print(res.first())

asyncio.run(get_all())