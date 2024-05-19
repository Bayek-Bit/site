from fastapi import APIRouter, Depends

from datetime import datetime

from auth.base_config import fastapi_users
from auth.models import User

student_router = APIRouter(
    prefix="/diary/student",
    tags=["StudentDiary"]
)

current_user = fastapi_users.current_user()


@student_router.get("/diary/get_students_timetable/{user_id}/{week_start}/{week_end}")
async def get_timetable(
        week_start: datetime,
        week_end: datetime,
        user: User = Depends(current_user)
):
    if user.role_id == 2:
        timetable = await AsyncORM.get_timetable_and_marks_by_week(user.id, week_start, week_end)
        return timetable
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can access this resource.")


@student_router.get("/diary/get_students_marks_table/{subject_id}/{class_id}/{date_from}/{date_to}")
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
