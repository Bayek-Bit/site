import asyncio
from typing import Optional

from fastapi import FastAPI, Depends, Request, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from fastapi_users import fastapi_users, FastAPIUsers

import uvicorn

# Queries
from db.queries.orm import AsyncORM
from db.queries.core import Core

# user manager
from auth.manager import get_user_manager

# schemas
from auth.schemas import UserCreate, UserRead

# auth
from auth.base_config import auth_backend, fastapi_users
from auth.models import User

# datetime как тип данных для передачи даты (год, месяц, день)
from datetime import datetime

from teacher_diary.schemas import MarkAddDTO, MarkUpdateDTO

# Teacher
from teacher_diary.router import teacher_router

# Student
from student_diary.router import student_router


async def main():

    pass


def create_fastapi_app():
    app = FastAPI(
        title="Diary"
    )

    # Зависит от порта фронта
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    current_user = fastapi_users.current_user()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "DELETE", "PATCH", "PUT"],
        allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                       "Authorization"],
    )

    app.include_router(
        fastapi_users.get_auth_router(auth_backend),
        prefix="/auth/jwt",
        tags=["auth"],
    )

    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix="/auth",
        tags=["auth"],
    )

    app.include_router(teacher_router)

    app.include_router(student_router)

    @app.get("/refresh")
    async def protected_route(user: User = Depends(current_user)):
        return {"username": user.username,
                "is_active": user.is_active,
                "role_id": user.role_id}

    return app


app = create_fastapi_app()

if __name__ == '__main__':
    asyncio.run(main())
    uvicorn.run(
        app="main:app",
        reload=True
    )
