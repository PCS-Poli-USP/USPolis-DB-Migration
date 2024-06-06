from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from server.models.database.reservation_db_model import Reservation
from server.models.database.schedule_calendar_link import ScheduleCalendarLink

if TYPE_CHECKING:
    from server.models.database.calendar_db_model import Calendar
    from server.models.database.class_db_model import Class
    from server.models.database.occurence_db_model import Ocurrence

from server.utils.day_time import DayTime
from server.utils.enums.recurrence import Recurrence
from server.utils.enums.week_day import WeekDay


class Schedule(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    week_day: WeekDay = Field()
    start_date: datetime = Field()
    end_date: datetime = Field()
    start_time: DayTime = Field()
    end_time: DayTime = Field()
    skip_exceptions: bool = Field(default=False)
    allocated: bool = Field(default=False)
    recurrence: Recurrence = Field()
    all_day: bool = Field(default=False)

    university_class_id: int | None = Field(foreign_key="class.id")
    university_class: "Class" = Relationship(back_populates="schedules")
    occurences: list["Ocurrence"] = Relationship(back_populates="schedule")
    calendars: list["Calendar"] = Relationship(
        back_populates="schedules", link_model=ScheduleCalendarLink
    )
    reservation: Reservation | None = Relationship(back_populates="schedule")
