from datetime import datetime

from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, field_validator, ValidationInfo


class MarkAddDTO(BaseModel):
    students_user_id: int
    teachers_user_id: int
    subject_id: int
    attendance: Optional[str]
    mark: Optional[int]

    set_date: datetime

    @field_validator('mark')
    @classmethod
    def mark_validate(cls, value, info: ValidationInfo):
        if isinstance(value, int):
            if value not in [2, 3, 4, 5]:
                raise ValueError("incorrect input data")
            else:
                return value
        if value is None:
            if info.data.get("attendance") is None:
                raise ValueError("incorrect input data. Mark and Attendance cant be NoneType both.")
        else:
            raise TypeError("incorrect type")

    @field_validator('attendance')
    @classmethod
    def attendance_validate(cls, value, info: ValidationInfo):
        if isinstance(value, str):
            if value not in ["н", "б", "п"]:
                raise ValueError("incorrect input data. Attendance should be only 'н', 'б' or 'п'.")
            else:
                return value
        if value is None:
            if info.data.get("mark") is None:
                raise ValueError("incorrect input data. Mark and Attendance cant be NoneType both.")


class MarkUpdateDTO(BaseModel):
    students_user_id: int
    teachers_user_id: int
    subject_id: int
    mark_id: int

    updated_mark: int
    update_date: datetime

    @field_validator('updated_mark')
    @classmethod
    def mark_validate(cls, value):
        if isinstance(value, int):
            if value not in [2, 3, 4, 5]:
                raise ValueError("incorrect input data")
        # if isinstance(value, str):
        #     if value not in ["н", "б", "п"]:
        #         raise ValueError("incorrect input data")
        else:
            raise TypeError("incorrect type")

        return value


class MarkDTO(MarkAddDTO):
    update_date: Optional[datetime]
