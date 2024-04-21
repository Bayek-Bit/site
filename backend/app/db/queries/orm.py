from sqlalchemy import Integer, insert, select, text
from sqlalchemy.orm import selectinload, joinedload

from database import Base, engine, async_session_factory
from auth.models import User
from models.database_model import Student, Teacher, TeacherClass, Class


class AsyncORM:
    @staticmethod
    async def create_tables():
        async with engine.begin() as conn:
            engine.echo = False
            await conn.run_sync(Base.metadata.create_all)
            engine.echo = True

    @staticmethod
    async def select_teachers():
        async with async_session_factory() as session:
            query = select(Teacher)
            result = await session.execute(query)
            teachers = result.scalars().all()
            print(f"Teachers={teachers}")

    # Получаем классы, которые обучает учитель. Example: {1: '6A', 2: '10A', 5: '2А'}
    @staticmethod
    async def get_classes_by_teacher_id(teacher_id: int) -> dict:
        classes_dict = {}

        async with async_session_factory() as session:
            stmt = (
                select(TeacherClass)
                .where(TeacherClass.teacher_id == teacher_id)
                .options(joinedload(TeacherClass.Class))
            )

            result = await session.execute(stmt)
            result = result.scalars().all()

            for teacher_class in result:
                class_id = teacher_class.Class.id
                class_name = teacher_class.Class.name
                classes_dict[class_id] = class_name

        return classes_dict

    # @staticmethod
    # async def get_students_in_class(teacher_id, class_id):
    #     async with async_session_factory() as session:
    #         query = select(Student).where()
