from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    username: str
    role_id: int


class UserCreate(schemas.BaseUserCreate):
    username: str
    role_id: int


# May be a bit later
# class UserUpdate(schemas.BaseUserUpdate):
#     pass