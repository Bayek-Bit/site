import datetime

from typing import Annotated

from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, MetaData, text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )]


class Users(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[str]
    password: Mapped[str]


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





# metadata_obj = MetaData()

# users_table = Table(
#     "users",
#     metadata_obj,
#     Column("username", String),
#     Column("password", String),
#     Column("role", String)
# )

# classes_table = Table(
#     "classes",
#     metadata_obj,
#     Column("name", String)
# )

# students_table = Table(
#     "students",
#     metadata_obj,
#     Column("user_id", Integer, ForeignKey("users.id"))
# )