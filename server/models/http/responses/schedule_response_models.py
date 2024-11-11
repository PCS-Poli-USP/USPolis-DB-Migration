from datetime import date, time

from pydantic import BaseModel

from server.models.database.schedule_db_model import Schedule
from server.models.http.exceptions.responses_exceptions import UnfetchDataError
from server.models.http.responses.occurrence_response_models import OccurrenceResponse
from server.utils.enums.month_week import MonthWeek
from server.utils.enums.recurrence import Recurrence
from server.utils.enums.week_day import WeekDay
from server.utils.must_be_int import must_be_int


class ScheduleResponseBase(BaseModel):
    id: int
    week_day: WeekDay | None = None
    month_week: MonthWeek | None = None
    start_date: date
    end_date: date
    start_time: time
    end_time: time
    allocated: bool
    recurrence: Recurrence
    all_day: bool

    class_id: int | None = None
    subject: str | None = None
    class_code: str | None = None

    reservation_id: int | None = None
    reservation: str | None = None

    classroom_id: int | None = None
    classroom: str | None = None

    building_id: int | None = None
    building: str | None = None

    @classmethod
    def from_schedule(cls, schedule: Schedule) -> "ScheduleResponseBase":
        return cls(
            id=must_be_int(schedule.id),
            week_day=schedule.week_day,
            month_week=schedule.month_week,
            start_date=schedule.start_date,
            end_date=schedule.end_date,
            start_time=schedule.start_time,
            end_time=schedule.end_time,
            allocated=schedule.allocated,
            recurrence=schedule.recurrence,
            all_day=schedule.all_day,
            classroom_id=schedule.classroom_id,
            classroom=schedule.classroom.name if schedule.classroom else None,
            building_id=schedule.classroom.building.id if schedule.classroom else None,
            building=schedule.classroom.building.name if schedule.classroom else None,
            class_id=schedule.class_id,
            subject=schedule.class_.subject.name if schedule.class_ else None,
            class_code=schedule.class_.code if schedule.class_ else None,
            reservation_id=schedule.reservation.id if schedule.reservation else None,
            reservation=schedule.reservation.title if schedule.reservation else None,
        )


class ScheduleResponse(ScheduleResponseBase):
    occurrence_ids: list[int] | None = None
    # When recurrence is custom is necessary
    occurrences: list[OccurrenceResponse] | None = None

    @classmethod
    def from_schedule(cls, schedule: Schedule) -> "ScheduleResponse":
        base = ScheduleResponseBase.from_schedule(schedule)
        return cls(
            **base.model_dump(),
            occurrence_ids=cls.get_occurences_ids(schedule)
            if schedule.occurrences and schedule.recurrence == Recurrence.CUSTOM
            else None,
            occurrences=OccurrenceResponse.from_occurrence_list(schedule.occurrences)
            if schedule.occurrences and schedule.recurrence == Recurrence.CUSTOM
            else None,
        )

    @classmethod
    def from_schedule_list(cls, schedules: list[Schedule]) -> list["ScheduleResponse"]:
        return [cls.from_schedule(schedule) for schedule in schedules]

    @classmethod
    def get_occurences_ids(cls, schedule: Schedule) -> list[int]:
        if schedule.occurrences is None:
            return []
        ids = []
        for occurence in schedule.occurrences:
            if occurence.id is None:
                raise UnfetchDataError("Ocurrence", "ID")
            ids.append(occurence.id)
        return ids


class ScheduleFullResponse(ScheduleResponseBase):
    """Schedules with occurrences not optional"""

    occurrences: list[OccurrenceResponse]

    @classmethod
    def from_schedule(cls, schedule: Schedule) -> "ScheduleFullResponse":
        base = ScheduleResponseBase.from_schedule(schedule)
        return cls(
            **base.model_dump(),
            occurrences=OccurrenceResponse.from_occurrence_list(schedule.occurrences)
            if schedule.occurrences
            else [],
        )

    @classmethod
    def from_schedule_list(
        cls, schedules: list[Schedule]
    ) -> list["ScheduleFullResponse"]:
        return [cls.from_schedule(schedule) for schedule in schedules]
