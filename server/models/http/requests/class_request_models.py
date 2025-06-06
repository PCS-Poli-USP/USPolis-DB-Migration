from datetime import datetime
from typing import Self
from fastapi import HTTPException, status
from pydantic import BaseModel, model_validator

from server.models.http.requests.schedule_request_models import (
    ScheduleRegister,
    ScheduleUpdate,
)
from server.utils.enums.audiovisual_type_enum import AudiovisualType
from server.utils.enums.class_type import ClassType


class ClassRequestBase(BaseModel):
    """Base for any Class request of register or update"""

    calendar_ids: list[int]
    start_date: datetime
    end_date: datetime
    code: str
    type: ClassType
    professors: list[str]
    vacancies: int

    air_conditionating: bool
    accessibility: bool
    audiovisual: AudiovisualType
    ignore_to_allocate: bool


class ClassRegister(ClassRequestBase):
    """Class register input body"""

    subject_id: int
    schedules_data: list[ScheduleRegister]

    @model_validator(mode="after")
    def check_class_body(self) -> Self:
        subject_id = self.subject_id
        schedules_data = self.schedules_data

        if subject_id <= 0:
            raise ClassInvalidData("Subject ID")
        if not schedules_data:
            raise ClassInvalidData("Schedules Data")
        return self


class ClassUpdate(ClassRequestBase):
    """Class update input body"""

    subject_id: int
    schedules_data: list[ScheduleUpdate]

    @model_validator(mode="after")
    def check_class_body(self) -> Self:
        subject_id = self.subject_id
        schedules_data = self.schedules_data

        if subject_id <= 0:
            raise ClassInvalidData("Subject ID")
        if not schedules_data:
            raise ClassInvalidData("Schedules Data")
        return self


class ClassInvalidData(HTTPException):
    def __init__(self, data_info: str) -> None:
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            f"Class has invalid {data_info} value",
        )


class ClassConflictedData(HTTPException):
    def __init__(self, first_data: str, second_data: str) -> None:
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            f"Schedule must have {first_data} value or {second_data} value, not both",
        )
