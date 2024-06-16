from datetime import datetime

from pydantic import BaseModel

from server.utils.day_time import DayTime
from server.utils.enums.class_type import ClassType
from server.utils.enums.week_day import WeekDay


class GeneralInfo(BaseModel):
    class_code: str
    start_date: datetime
    end_date: datetime
    class_type: ClassType
    obs: str | None


class ScheduleInfo(BaseModel):
    week_day: WeekDay
    professors: list[str]
    start_time: DayTime
    end_time: DayTime


class StudentNumbersInfo(BaseModel):
    vacancies: int
    subscribers: int
    pendings: int
    enrolled: int
