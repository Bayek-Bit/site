# statement for insert/update/delete 
# query for select
from typing import Annotated, AsyncGenerator

from sqlalchemy import String, text, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import settings


str_256 = Annotated[str, 256]

class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }


engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True
)
async_session_factory = async_sessionmaker(engine)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session