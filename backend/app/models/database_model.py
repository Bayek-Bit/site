import datetime

from typing import Annotated, List, Optional

from fastapi_users.db import SQLAlchemyBaseUserTable

from sqlalchemy import text, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.now(datetime.timezone.utc),
)]


class Role(Base):
    __tablename__ = "role"

    id: Mapped[intpk]
    name: Mapped[str]


class TeacherClass(Base):
    __tablename__ = "teacher_class"

    id: Mapped[intpk]

    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"))
    class_id: Mapped[int] = mapped_column(ForeignKey("class.id"))


class Class(Base):
    __tablename__ = "class"

    id: Mapped[intpk]
    name: Mapped[str]

    teachers = relationship("Teacher", secondary="teacher_class")
    # teachers: Mapped[list["TeacherClass"]] = relationship("TeacherClass", back_populates="class_")


class Student(Base):
    __tablename__ = "student"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    first_name: Mapped[str]
    last_name: Mapped[str]
    father_name: Mapped[str]
    class_id: Mapped[int] = mapped_column(ForeignKey("class.id", ondelete="CASCADE"))


class Teacher(Base):
    __tablename__ = "teacher"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    first_name: Mapped[str]
    last_name: Mapped[str]
    father_name: Mapped[str]
    # В secondary указывается именно название таблицы (__tablename__)
    classes_taught = relationship("Class", secondary="teacher_class", overlaps="teachers")

    lessons: Mapped[list["Timetable"]] = relationship("Timetable", back_populates="Teacher")


class Subject(Base):
    __tablename__ = "subject"

    id: Mapped[intpk]
    name: Mapped[str]

    marks: Mapped[list["Mark"]] = relationship("Mark", back_populates="Subject", lazy="dynamic")


class Timetable(Base):
    __tablename__ = "timetable"

    id: Mapped[intpk]
    day_of_week: Mapped[str]
    class_id: Mapped[int] = mapped_column(ForeignKey("class.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"))
    lesson_number: Mapped[int]
    classroom_number: Mapped[int]
    start_time: Mapped[str]
    end_time: Mapped[str]
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"))

    Teacher: Mapped["Teacher"] = relationship("Teacher")
    Subject: Mapped["Subject"] = relationship("Subject")


class Mark(Base):
    __tablename__ = "mark"

    id: Mapped[intpk]
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"))
    mark: Mapped[int]
    set_date: Mapped[datetime.datetime]

    Subject: Mapped["Subject"] = relationship("Subject", back_populates="marks")
