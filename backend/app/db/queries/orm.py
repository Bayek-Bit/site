from sqlalchemy import Integer, insert, select, text
from sqlalchemy.orm import selectinload, joinedload

from database import Base, engine, async_session_factory
from auth.models import User
from models.database_model import Student, Teacher, TeacherClass, Class, Timetable, Mark

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

    # Student Функция возвращает словарь - расписание на неделю.
    # На каждый день недели - свое кол-во уроков.
    # У каждой записи есть номер урока по счёту, время начала-конца, название и имя учителя
    # Example:
    # {'Вторник': [(1, '8:00', '8:40', 'Математика', 'Math Math Math`s')],
    # 'Понедельник': [(1, '8:00', '8:40', 'Математика', 'Math Math Math`s'), (2,
    # '8:50', '9:30', 'Математика', 'Math Math Math`s'), (3, '9:40', '10:20', 'Русский язык', 'Rus Rus Russian'), (4,
    # '10:40', '11:20', 'Русский язык', 'Rus Rus Russian'), (5, '11:40', '12:20', 'Литература', 'Lit Lit Literature')]}
    @staticmethod
    async def get_timetable_and_marks_by_week(class_id: int, week_start: datetime, week_end: datetime):
        timetable_dict = defaultdict(list)

        async with async_session_factory() as session:
            # Получаем расписание класса
            timetable_query = (
                select(Timetable)
                .where(Timetable.class_id == class_id)
                .options(joinedload(Timetable.Teacher), joinedload(Timetable.Subject))
            )

            timetable_result = await session.execute(timetable_query)
            timetable_result = timetable_result.scalars().all()

            # Получаем оценки
            query = (
                select(Mark)
                .where(Mark.set_date >= week_start, Mark.set_date <= week_end)
                .options(joinedload(Mark.Subject))
            )

            marks_result = await session.execute(query)
            marks_result = marks_result.scalars().all()

            week_days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

            for timetable_obj in timetable_result:
                # Extract relevant information from the timetable object
                day_of_week = timetable_obj.day_of_week
                subject_name = timetable_obj.Subject.name
                teacher_name = f"{timetable_obj.Teacher.first_name} {timetable_obj.Teacher.last_name} {timetable_obj.Teacher.father_name}"
                lesson_number = timetable_obj.lesson_number
                start_time = timetable_obj.start_time
                end_time = timetable_obj.end_time

                # Add subject details to the list for the day of the week
                timetable_dict[day_of_week].append({
                    'lesson_number': lesson_number,
                    'start_time': start_time,
                    'end_time': end_time,
                    'subject_name': subject_name,
                    'teacher_name': teacher_name,
                    'marks': []  # Placeholder for marks
                })

            for mark in marks_result:
                week_day = week_days[mark.set_date.day - week_start.day]
                subject_name = mark.Subject.name
                mark_info = mark.mark
                for lesson in timetable_dict[week_day]:
                    if lesson["subject_name"] == subject_name:
                        print(lesson)
                        lesson["marks"].append(mark_info)
                        break

        return timetable_dict

    # @staticmethod
    # async def get_timetable(class_id: int):
    #     timetable_dict = defaultdict(list)
    #
    #     async with async_session_factory() as session:
    #         query = (
    #             select(Timetable)
    #             .where(Timetable.class_id == class_id)
    #             .options(joinedload(Timetable.Teacher), joinedload(Timetable.Subject))
    #         )
    #
    #         result = await session.execute(query)
    #         result = result.scalars().all()
    #
    #         for timetable_obj in result:
    #             # Extract relevant information from the timetable object
    #             day_of_week = timetable_obj.day_of_week
    #             subject_name = timetable_obj.Subject.name
    #             lesson_number = timetable_obj.lesson_number
    #             start_time = timetable_obj.start_time
    #             end_time = timetable_obj.end_time
    #
    #             # Add subject details to the list for the day of the week
    #             timetable_dict[day_of_week].append((lesson_number, start_time, end_time, subject_name))
    #
    #             # Sort subjects within each day by lesson number
    #         for day, subjects in timetable_dict.items():
    #             subjects.sort(key=lambda x: x[0])  # Sort by lesson number (index 0)
    #
    #             # Convert defaultdict to a regular dictionary
    #         timetable_dict = dict(timetable_dict)
    #         print(timetable_dict)

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
