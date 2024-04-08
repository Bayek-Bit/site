import datetime

from typing import Annotated

from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, Date, Time, MetaData, text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base

import enum


intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
    )]


class Roles(Base):
    __tablename__ = "roles"

    id: Mapped[intpk]
    name: Mapped[str]

class Users(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[str]
    password: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))



class Classes(Base):
    __tablename__ = "classes"

    id: Mapped[intpk]
    name: Mapped[str]

class Students(Base):
    __tablename__ = "students"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    first_name: Mapped[str]
    last_name: Mapped[str]
    father_name: Mapped[str]
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id", ondelete="CASCADE"))


class Teachers(Base):
    __tablename__ = "teachers"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    first_name: Mapped[str]
    last_name: Mapped[str]
    father_name: Mapped[str]

class Teachers_classes(Base):
    __tablename__ = "teachers"
    
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"))

class Subjects(Base):
    __tablename__ = "subjects"
    
    id: Mapped[intpk]
    name: Mapped[str]

class Timetable(Base):
    __tablename__ = "timetable"
    
    id: Mapped[intpk]
    day_of_week: Mapped[str]
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
    start_time: Mapped[Time]
    end_time: Mapped[Time]
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))

class Marks(Base):
    id: Mapped[intpk]
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
    mark: Mapped[int]
    set_date: Mapped[Date]