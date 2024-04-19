from fastapi_users.db import SQLAlchemyBaseUserTable

from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    role_id: Mapped[int]