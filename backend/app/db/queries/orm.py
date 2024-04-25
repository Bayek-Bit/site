from sqlalchemy import Integer, insert, select, text
from sqlalchemy.orm import selectinload, joinedload

from database import Base, engine, async_session_factory
from auth.models import User
from models.database_model import Student, Teacher, TeacherClass, Class, Timetable

from datetime import datetime

from collections import defaultdict


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

    # Student
    # Функция возвращает словарь - расписание на неделю.
    @staticmethod
    async def get_timetable(class_id: int):
        timetable_dict = defaultdict(list)

        async with async_session_factory() as session:
            query = (
                select(Timetable)
                .where(Timetable.class_id == class_id)
                .options(joinedload(Timetable.Teacher), joinedload(Timetable.Subject))
            )

            result = await session.execute(query)
            result = result.scalars().all()

            for timetable_obj in result:
                # Extract relevant information from the timetable object
                day_of_week = timetable_obj.day_of_week
                subject_name = timetable_obj.Subject.name
                start_time = timetable_obj.start_time
                end_time = timetable_obj.end_time

                # Add subject details to the list for the day of the week
                timetable_dict[day_of_week].append((subject_name, start_time, end_time))

                # Sort subjects by start time
            for day, subjects in timetable_dict.items():
                timetable_dict[day] = sorted(subjects, key=lambda x: x[1])  # Sorting by start time

                # Convert defaultdict to a regular dictionary
            timetable_dict = dict(timetable_dict)
            print(timetable_dict)

    # Получаем классы, которые обучает учитель. Example: {1: '6A', 2: '10A', 5: '2А'}
    @staticmethod
    async def get_classes_by_teacher_id(teacher_id: int) -> dict:
        classes_dict = {}

        async with async_session_factory() as session:
            query = (
                select(TeacherClass)
                .where(TeacherClass.teacher_id == teacher_id)
                .options(joinedload(TeacherClass.Class))
            )

            result = await session.execute(query)
            result = result.scalars().all()

            for teacher_class in result:
                class_id = teacher_class.Class.id
                class_name = teacher_class.Class.name
                classes_dict[class_id] = class_name

        return classes_dict

    @staticmethod
    async def get_students_in_class(class_id: int):
        async with async_session_factory() as session:
            query = select(Student).where(Student.class_id == class_id)

            result = await session.execute(query)
            result = result.scalars().all()

            return result
