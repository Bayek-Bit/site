from sqlalchemy import Integer, insert, update, select, text, and_
from sqlalchemy.orm import selectinload, joinedload, with_loader_criteria
from sqlalchemy.orm.exc import NoResultFound

from database import Base, engine, async_session_factory

from models.database_model import Student, Teacher, TeacherClass, Class, Timetable, Mark, TeacherSubject, Subject

from datetime import datetime

from collections import defaultdict

from typing import Optional

import json


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

    # (Teacher)
    # Оценки
    @staticmethod
    async def set_mark(teachers_user_id: int, students_user_id: int, subject_id: int, set_date: datetime,
                       attendance: Optional[str] = None, mark: Optional[int] = None):
        async with async_session_factory() as session:
            # Ищем учителя, присоединяя предметы, которым он обучает, и классы, которые он обучает.
            teacher_query = (
                select(Teacher)
                .where(Teacher.user_id == teachers_user_id)
                .options(joinedload(Teacher.taught_subjects))
                .options(joinedload(Teacher.classes_taught))
            )
            try:
                teacher = await session.execute(teacher_query)
                teacher = teacher.unique().scalars().one()
            except NoResultFound:
                return {"error": "Not allowed."}
            # Получаем студента, подгружая класс, в котором он обучается
            try:
                student = await session.execute(
                    select(Student).where(Student.user_id == students_user_id).options(joinedload(Student.class_)))
                student = student.scalars().one()
            except NoResultFound:
                return {"error": "Student not found."}

            # id Класса, в котором обучается студент
            student_class_id = student.class_.id

            # id всех предметов, которым обучает учитель
            ts_ids = [ts.id for ts in teacher.taught_subjects]
            # id всех классов, которые обучает учитель
            tc_ids = [tc.id for tc in teacher.classes_taught]

            if (student_class_id in tc_ids) and (subject_id in ts_ids):
                stmt = (
                    insert(Mark).
                    values(
                        student_id=student.id,
                        teacher_id=teacher.id,
                        subject_id=subject_id,
                        attendance=attendance,
                        mark=mark,
                        set_date=set_date  # Над датой нужно подумать
                    )
                )
                await session.execute(stmt)
                await session.commit()

    @staticmethod
    async def update_mark(teachers_user_id: int, students_user_id: int, subject_id: int, mark_id: int,
                          updated_mark: int, update_date: datetime):
        async with async_session_factory() as session:
            # Ищем учителя, присоединяя предметы, которым он обучает, и классы, которые он обучает.
            teacher_query = (
                select(Teacher)
                .where(Teacher.user_id == teachers_user_id)
                .options(joinedload(Teacher.taught_subjects))
                .options(joinedload(Teacher.classes_taught))
            )
            try:
                result = await session.execute(teacher_query)
                result = result.unique().scalars().one()
            except NoResultFound:
                return {"error": "Not allowed."}
            # Получаем студента, подгружая класс, в котором он обучается
            try:
                student = await session.execute(
                    select(Student).where(Student.user_id == students_user_id).options(joinedload(Student.class_)))
                student = student.scalars().one()
            except NoResultFound:
                return {"error": "Student not found."}

            # id Класса, в котором обучается студент
            student_class_id = student.class_.id

            # id всех предметов, которым обучает учитель
            ts_ids = [ts.id for ts in result.taught_subjects]
            # id всех классов, которые обучает учитель
            tc_ids = [tc.id for tc in result.classes_taught]

            if (student_class_id in tc_ids) and (subject_id in ts_ids):
                stmt = (
                    update(Mark)
                    .where(Mark.id == mark_id)
                    .values(
                        mark=updated_mark,
                        update_date=update_date
                    )
                )
                await session.execute(stmt)
                await session.commit()

    # Функция позволяет получить оценки всех студентов в классе.
    @staticmethod
    async def get_students_marks_table(
            teachers_user_id: int,
            subject_id: int,
            class_id: int,
            date_from: datetime,
            date_to: datetime
    ):
        async with async_session_factory() as session:
            teacher_query = (
                select(Teacher)
                .where(Teacher.user_id == teachers_user_id)
                .options(selectinload(Teacher.classes_taught).selectinload(Class.students).selectinload(Student.marks),
                         with_loader_criteria(Mark, and_(Mark.set_date >= date_from, Mark.set_date <= date_to, Mark.subject_id == subject_id)))
            )
            teacher = await session.execute(teacher_query)
            teacher = teacher.scalars().one()

            current_class = None
            for i in teacher.classes_taught:
                if i.id == class_id:
                    current_class = i
                    break

            if current_class:
                return current_class

    # Классы, которые обучает учитель
    @staticmethod
    async def get_classes(user_id: int):
        async with async_session_factory() as session:
            teacher_query = (
                select(Teacher)
                .where(Teacher.user_id == user_id)
                .options(selectinload(Teacher.classes_taught))
            )
            teacher = await session.execute(teacher_query)
            teacher = teacher.scalars().one()
            return teacher.classes_taught

    # Учитель может получить своё расписание.
    @staticmethod
    async def get_teachers_timetable(user_id: int):
        async with async_session_factory() as session:
            teacher_timetable_query = (
                select(Teacher)
                .where(Teacher.user_id == user_id)
                .options(selectinload(Teacher.lessons).selectinload(Timetable.Subject))
            )

            timetable_result = await session.execute(teacher_timetable_query)
            timetable_result = timetable_result.scalars().one()

            lessons = timetable_result.lessons

            lessons_json = []
            for lesson in lessons:
                lesson_dict = {
                    "id": lesson.id,
                    "day_of_week": lesson.day_of_week,
                    "class_id": lesson.class_id,
                    "teacher_id": lesson.teacher_id,
                    "lesson_number": lesson.lesson_number,
                    "classroom_number": lesson.classroom_number,
                    "start_time": lesson.start_time,
                    "end_time": lesson.end_time,
                    "subject": {
                        "id": lesson.Subject.id,
                        "name": lesson.Subject.name
                    }
                }
                lessons_json.append(lesson_dict)

            # Преобразование списка словарей в JSON-строку
            timetable_json_str = json.dumps(lessons_json)

            return timetable_json_str

    # (Student)
    # Функция возвращает словарь - расписание на неделю.
    # На каждый день недели - свое кол-во уроков.
    # У каждой записи есть номер урока по счёту, время начала-конца, название предмета, имя учителя и кабинет
    @staticmethod
    async def get_timetable_and_marks_by_week(user_id: int, week_start: datetime, week_end: datetime):
        timetable_dict = defaultdict(list)

        async with async_session_factory() as session:
            # Получаем расписание класса
            student_timetable_query = (
                select(Timetable)
                .join(Student, Timetable.class_id == Student.class_id)
                .where(Student.user_id == user_id)
                .options(joinedload(Timetable.Teacher), joinedload(Timetable.Subject))
            )

            timetable_result = await session.execute(student_timetable_query)
            timetable_result = timetable_result.scalars().all()

            # Получаем оценки
            mark_query = (
                select(Mark)
                .join(Student, Mark.student_id == Student.id)
                .where(Student.user_id == user_id, Mark.set_date >= week_start, Mark.set_date <= week_end)
                .options(joinedload(Mark.Subject))
            )

            marks_result = await session.execute(mark_query)
            marks_result = marks_result.scalars().all()

            week_days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

            for timetable_obj in timetable_result:
                # Extract relevant information from the timetable object
                day_of_week = timetable_obj.day_of_week
                subject_name = timetable_obj.Subject.name
                teacher_name = f"{timetable_obj.Teacher.first_name} {timetable_obj.Teacher.last_name} {timetable_obj.Teacher.father_name}"
                lesson_number = timetable_obj.lesson_number
                classroom_number = timetable_obj.classroom_number
                start_time = timetable_obj.start_time
                end_time = timetable_obj.end_time

                # Add subject details to the list for the day of the week
                timetable_dict[day_of_week].append({
                    'lesson_number': lesson_number,
                    'start_time': start_time,
                    'end_time': end_time,
                    'subject_name': subject_name,
                    'teacher_name': teacher_name,
                    'classroom_number': classroom_number,
                    'marks': []  # Placeholder for marks
                })

            for mark in marks_result:
                week_day = week_days[mark.set_date.day - week_start.day]
                subject_name = mark.Subject.name
                mark_info = [mark.mark, mark.id]
                for lesson in timetable_dict[week_day]:
                    if lesson["subject_name"] == subject_name:
                        lesson["marks"].append(mark_info)
                        break

        return timetable_dict

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
