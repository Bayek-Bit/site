# set limit to all varchar`s

import datetime

from typing import Annotated

from fastapi_users.db import SQLAlchemyBaseUserTable

from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, Date, Time, MetaData, text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base



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

# class Users(Base):
#     __tablename__ = "users"

#     id: Mapped[intpk]
#     username: Mapped[str]
#     password: Mapped[str]
#     role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))

class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[intpk]
    username: Mapped[str]
    email: Mapped[str]
    hashed_password: Mapped[str]
    is_active: Mapped[bool]
    is_superuser: Mapped[bool]
    is_verified: Mapped[bool]


class Class(Base):
    __tablename__ = "class"

    id: Mapped[intpk]
    name: Mapped[str]


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

class Teacher_class(Base):
    __tablename__ = "teacher_class"

    id: Mapped[intpk]
    
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"))
    class_id: Mapped[int] = mapped_column(ForeignKey("class.id"))

class Subject(Base):
    __tablename__ = "subject"
    
    id: Mapped[intpk]
    name: Mapped[str]

class Timetable(Base):
    __tablename__ = "timetable"
    
    id: Mapped[intpk]
    day_of_week: Mapped[str]
    class_id: Mapped[int] = mapped_column(ForeignKey("class.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"))
    start_time: Mapped[str]
    end_time: Mapped[str]
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"))

class Mark(Base):
    __tablename__ = "mark"
    
    id: Mapped[intpk]
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"))
    mark: Mapped[int]
    set_date: Mapped[datetime.datetime]