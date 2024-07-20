

from datetime import date, datetime
from pydantic import BaseModel

from server.models.database.class_db_model import Class
from server.models.database.classroom_db_model import Classroom
from server.models.http.exceptions.responses_exceptions import UnfetchDataError
from server.routes.public.dtos.mobile_schedule_response import MobileScheduleResponse


class MobileClassResponse(BaseModel):
    id: int
    start_date: date
    end_date: date
    code: str
    professors: list[str]
    subject_name: str
    subject_code: str
    schedules: list[MobileScheduleResponse]
    
    @classmethod
    def from_model(cls, _class: Class) -> "MobileClassResponse":
        if _class.id is None:
            raise UnfetchDataError("Class", "ID")
        if _class.subject.id is None:
            raise UnfetchDataError("Subject", "ID")
        return cls(
            id=_class.id,
            start_date=_class.start_date,
            end_date=_class.end_date,
            code=_class.code,
            professors=_class.professors,
            subject_name=_class.subject.name,
            subject_code=_class.subject.code,
            schedules=MobileScheduleResponse.from_schedule_list(_class.schedules)
        )

    @classmethod
    def from_model_list(cls, classes: list[Class]):
        return [cls.from_model(u_class) for u_class in classes]