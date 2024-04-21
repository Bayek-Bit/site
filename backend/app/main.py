import asyncio
from typing import Optional

from fastapi import FastAPI, Depends, Request, Response, HTTPException, Cookie
from fastapi.middleware.cors import CORSMiddleware

from fastapi_users import fastapi_users, FastAPIUsers

import uvicorn

# Queries
from db.queries.orm import AsyncORM
from db.queries.core import Core

# user manager
from auth.manager import get_user_manager

# schema
from auth.schemas import UserCreate, UserRead

# auth
from auth.base_config import auth_backend, fastapi_users
from auth.models import User

# datetime как тип данных для передачи даты (год, месяц, день)
from datetime import datetime


async def main():
    # await Core.get_marks(1, week_start=datetime(2024, 4, 15), week_end=datetime(2024, 4, 19))
    await AsyncORM.create_tables()

def create_fastapi_app():
    app = FastAPI(
        title="Diary"
    )

    # Зависит от порта фронта
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

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

    current_user = fastapi_users.current_user()

    @app.get("/refresh")
    async def protected_route(user: User = Depends(current_user)):
        return {"username": user.username,
                "is_active": user.is_active,
                "role_id": user.role_id}

    @app.post("/diary/get_marks/{student_id}/{week_start}/{week_end}")
    async def protected_route(student_id: int, week_start: datetime, week_end: datetime,
                              user: User = Depends(current_user)):
        print(student_id, week_start, week_end)
        marks = await Core.get_marks(student_id=student_id, week_start=week_start, week_end=week_end)
        return marks

    return app


app = create_fastapi_app()

if __name__ == '__main__':
    asyncio.run(main())
    uvicorn.run(
        app="main:app",
        reload=True
    )
