from fastapi import APIRouter, Depends

from datetime import datetime


from auth.base_config import fastapi_users
from auth.models import User


from teacher_diary.schemas import MarkAddDTO, MarkUpdateDTO

teacher_router = APIRouter(
    prefix="/diary/teacher",
    tags=["TeacherDiary"]
)


current_user = fastapi_users.current_user()


@teacher_router.get("/get_teachers_timetable")
async def get_teachers_timetable(user: User = Depends(current_user)):
    if user.role_id == 3:
        teachers_timetable = await AsyncORM.get_teachers_timetable(user.id)
        return teachers_timetable
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only teachers can access this resource.")


@teacher_router.get("/get_classes")
async def get_classes(user: User = Depends(current_user)):
    if user.role_id == 3:
        classes = await AsyncORM.get_classes(user_id=user.id)
        return classes
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only teachers can access this resource.")

    # Only teacher can get students list like this. (In future) Admin also can use this


@teacher_router.get("/get_students_by_class/{class_id}")
async def get_students(class_id: int, user: User = Depends(current_user)):
    if user.role_id == 3:
        students = await AsyncORM.get_students_in_class(class_id)
        return students
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only teachers can access this resource.")


@teacher_router.post("/set_mark", tags=["Marks"])
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
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only teachers can access this resource.")


@teacher_router.post("/update_mark", tags=["Marks"])
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
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only teachers can access this resource.")


@teacher_router.get("/get_students_marks_table/{subject_id}/{class_id}/{date_from}/{date_to}")
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
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only teachers can access this resource.")
