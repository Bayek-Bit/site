import datetime

from typing import Annotated, List, Optional

from fastapi_users.db import SQLAlchemyBaseUserTable

from sqlalchemy import CheckConstraint, text, String, Integer
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

    students = relationship("Student", back_populates="class_")

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

    class_ = relationship("Class", back_populates="students")

    marks = relationship("Mark", back_populates="student")


class Teacher(Base):
    __tablename__ = "teacher"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    father_name: Mapped[str] = mapped_column(String(50))

    # Предметы, которым обучает учитель
    taught_subjects = relationship("TeacherSubject", back_populates="teacher")

    # В secondary указывается именно название таблицы (__tablename__)
    # Классы, которые обучает учитель
    classes_taught = relationship("Class", secondary="teacher_class", overlaps="teachers")

    # Расписание предметов, которым обучает учитель
    lessons = relationship("Timetable", back_populates="Teacher")

    # Оценки, которые поставил учитель по всем его предметам
    marks = relationship("Mark", back_populates="teacher", lazy="dynamic")


# for students
class Subject(Base):
    __tablename__ = "subject"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(100))

    teachers = relationship("TeacherSubject", back_populates="subject")

    marks = relationship("Mark", back_populates="subject", lazy="dynamic")


class TeacherSubject(Base):
    __tablename__ = "teacher_subject"

    id: Mapped[intpk]
    teacher_id: Mapped[int] = mapped_column(ForeignKey('teacher.id'))
    subject_id: Mapped[int] = mapped_column(ForeignKey('subject.id'))

    teacher = relationship("Teacher", back_populates="taught_subjects")
    subject = relationship("Subject", back_populates="teachers")


class Timetable(Base):
    __tablename__ = "timetable"

    id: Mapped[intpk]
    day_of_week: Mapped[str] = mapped_column(String(50))
    class_id: Mapped[int] = mapped_column(ForeignKey("class.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"))
    lesson_number: Mapped[int]
    classroom_number: Mapped[int]
    start_time: Mapped[str] = mapped_column(String(5))
    end_time: Mapped[str] = mapped_column(String(5))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"))

    Teacher = relationship("Teacher")
    Subject = relationship("Subject")


class Mark(Base):
    __tablename__ = "mark"

    id: Mapped[intpk]
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"))
    mark: Mapped[int]
    attendance: Mapped[Optional[str]] = mapped_column(String(1), nullable=True)
    set_date: Mapped[datetime.datetime]
    update_date: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)

    student = relationship("Student", back_populates="marks")
    teacher = relationship("Teacher", back_populates="marks")
    subject = relationship("Subject", back_populates="marks")

    __table_args__ = (
        CheckConstraint(
            '(mark IS NOT NULL AND attendance IS NULL) OR (mark IS NULL AND attendance IS NOT NULL)',
            name='check_mark_or_attendance'
        ),
    )


class Homework(Base):
    __tablename__ = "homework"

    id: Mapped[intpk]
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"))
    class_id: Mapped[int] = mapped_column(ForeignKey("class.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"))

    task: Mapped[str] = mapped_column(String(250))
