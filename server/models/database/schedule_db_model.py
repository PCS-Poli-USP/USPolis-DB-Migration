from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel

from server.models.database.reservation_db_model import Reservation
from server.models.database.schedule_calendar_link import ScheduleCalendarLink

if TYPE_CHECKING:
    from server.models.database.calendar_db_model import Calendar
    from server.models.database.class_db_model import Class
    from server.models.database.classroom_db_model import Classroom
    from server.models.database.occurrence_db_model import Occurrence

from server.utils.day_time import DayTime, DayTimeType
from server.utils.enums.recurrence import Recurrence
from server.utils.enums.week_day import WeekDay


class Schedule(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    start_date: date = Field()
    end_date: date = Field()
    start_time: DayTime = Field(sa_column=Column(DayTimeType, nullable=False))
    end_time: DayTime = Field(sa_column=Column(DayTimeType, nullable=False))
    skip_exceptions: bool = Field(default=False)
    allocated: bool = Field(default=False)
    recurrence: Recurrence = Field()
    week_day: WeekDay = Field()
    month_week: int | None = Field(default=None, nullable=True)
    all_day: bool = Field(default=False)

    class_id: int | None = Field(foreign_key="class.id", nullable=True, default=None)
    class_: Optional["Class"] = Relationship(back_populates="schedules")

    classroom_id: int | None = Field(
        foreign_key="classroom.id", nullable=True, default=None
    )
    classroom: Optional["Classroom"] = Relationship(back_populates="schedules")

    reservation: Optional["Reservation"] = Relationship(back_populates="schedule")

    occurrences: list["Occurrence"] = Relationship(back_populates="schedule")
    calendars: list["Calendar"] = Relationship(
        back_populates="schedules", link_model=ScheduleCalendarLink
    )
