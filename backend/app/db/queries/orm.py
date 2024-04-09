from sqlalchemy import Integer, insert, select, text


from db.database import Base, engine, async_session_factory
from models.database_model import Student, Teacher



class AsyncORM:
    @staticmethod
    async def create_tables():
        async with engine.begin() as conn:
            engine.echo = False
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            engine.echo = True

    @staticmethod
    async def select_teachers():
        async with async_session_factory() as session:
            query = select(Teacher)
            result = await session.execute(query)
            teachers = result.scalars().all()
            print(f"Teachers={teachers}")