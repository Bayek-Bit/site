from sqlalchemy import Integer, insert, select, text


from db.database import Base, engine, async_session_factory
from models.database_model import Students, Teachers



class AsyncORM:
    @staticmethod
    async def create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def select_teachers():
        async with async_session_factory as session:
            query = select(Teachers)
            result = session.execute(query)
            teachers = result.scalars().all()
            print(f"Teachers={teachers}")