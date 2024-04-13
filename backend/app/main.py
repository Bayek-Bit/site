import asyncio

from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware

from fastapi_users import fastapi_users, FastAPIUsers

import uvicorn

# database
from db.queries.orm import AsyncORM

#user manager
from db.manager import get_user_manager

#schema
from schemas.user_schema import UserCreate, UserRead

from db.database import User

#auth
from db.auth import auth_backend

#pydantic
from pydantic import BaseModel


async def main():
    # await AsyncORM.create_tables()
    await AsyncORM.select_teachers()




def create_fastapi_app():
    app = FastAPI(
        title="Diary"
    )
    
    fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
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
        allow_headers=["*"],
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

    # class ConfigData(BaseModel):
    #     data: str
    #     status: int
    #     statusText: str
    #     headers: dict
    #     config: dict
    #     request: dict

    @app.post("/diary/login")
    async def login(request: Request):
        data = await request.json()
        print(data)
        return "Hello"

    @app.get("/diary/refresh")
    async def refresh():
        return "Hello"
    
    @app.post("/diary/logout")
    async def logout():
        return "Logout"

    current_user = fastapi_users.current_user()

    @app.get("/protected-route")
    async def protected_route(user: User = Depends(current_user)):
        return f"Hello, {user.email}"

    return app

app = create_fastapi_app()  

if __name__ == '__main__':
    asyncio.run(main())
    uvicorn.run(
        app="main:app",
        reload=True
    )