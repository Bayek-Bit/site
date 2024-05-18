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

# schema
from auth.schemas import UserCreate, UserRead

# auth
from auth.base_config import auth_backend, fastapi_users
from auth.models import User

# datetime как тип данных для передачи даты (год, месяц, день)
from datetime import datetime

from teacher_diary.schemas import MarkAddDTO, MarkUpdateDTO


# teacher
# from teacher_diary import router as teacher_router


async def main():
    await AsyncORM.get_students_marks_table(teachers_user_id=3, subject_id=1, class_id=1,
                                            date_from=datetime(2024, 4, 15, 0,0,0,0), date_to=datetime(2024, 4, 16,0,0,0,0))
    # await AsyncORM.create_tables()
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

    # app.include_router(teacher_router)

    current_user = fastapi_users.current_user()

    @app.get("/refresh")
    async def protected_route(user: User = Depends(current_user)):
        return {"username": user.username,
                "is_active": user.is_active,
                "role_id": user.role_id}

    @app.post("/diary/get_teachers_timetable")
    async def get_teachers_timetable(user: User = Depends(current_user)):
        if user.role_id == 3:
            teachers_timetable = await AsyncORM.get_teachers_timetable(user.id)
            return teachers_timetable
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only teachers can access this resource.")

    @app.post("/diary/get_classes")
    async def get_classes(user: User = Depends(current_user)):
        if user.role_id == 3:
            classes = await AsyncORM.get_classes(user_id=user.id)
            return classes
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only teachers can access this resource.")

    # Only teacher can get students list like this. (In future) Admin also can use this
    @app.post("/diary/get_students_by_class/{class_id}")
    async def get_students(class_id: int, user: User = Depends(current_user)):
        if user.role_id == 3:
            students = await AsyncORM.get_students_in_class(class_id)
            return students
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only teachers can access this resource.")

    @app.post("/diary/set_mark")
    async def set_mark(mark: MarkAddDTO, user: User = Depends(current_user)):
        if user.role_id == 3:
            set_date = datetime.now()
            print(type(mark.mark))
            await AsyncORM.set_mark(
                teachers_user_id=mark.teachers_user_id,
                students_user_id=mark.students_user_id,
                subject_id=mark.subject_id,
                mark=mark.mark,
                set_date=set_date
            )
            return 200
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can access this resource.")

    @app.post("/diary/update_mark")
    async def update_mark(updated_mark_data: MarkUpdateDTO, user: User = Depends(current_user)):
        if user.role_id == 3:
            update_date = datetime.now()
            await AsyncORM.update_mark(
                teachers_user_id=updated_mark_data.teachers_user_id,
                students_user_id=updated_mark_data.students_user_id,
                subject_id=updated_mark_data.subject_id,
                mark_id=updated_mark_data.mark_id,
                updated_mark=updated_mark_data.updated_mark,
                update_date=update_date
            )
            return 200
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can access this resource.")

    @app.post("/diary/get_students_timetable/{user_id}/{week_start}/{week_end}")
    async def get_timetable(
            week_start: datetime,
            week_end: datetime,
            user: User = Depends(current_user)
    ):
        if user.role_id == 3:
            timetable = await AsyncORM.get_timetable_and_marks_by_week(user.id, week_start, week_end)
            return timetable
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can access this resource.")

    @app.post("/diary/get_students_marks_table/{subject_id}/{class_id}/{date_from}/{date_to}")
    async def get_students_marks_table(
            subject_id: int,
            class_id: int,
            date_from: datetime,
            date_to: datetime,
            user: User = Depends(current_user)
    ):
        if user.role_id == 3:
            table = await AsyncORM.get_students_marks_table(
                teachers_user_id=user.id,
                subject_id=subject_id,
                class_id=class_id,
                date_from=date_from,
                date_to=date_to
            )
            return table
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can access this resource.")

    return app


app = create_fastapi_app()

if __name__ == '__main__':
    asyncio.run(main())
    uvicorn.run(
        app="main:app",
        reload=True
    )
