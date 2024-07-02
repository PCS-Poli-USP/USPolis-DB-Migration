from fastapi import HTTPException, status
from httpx import delete
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, col, select

from server.models.database.building_db_model import Building
from server.models.database.class_db_model import Class
from server.models.database.schedule_db_model import Schedule
from server.models.http.requests.occurrence_request_models import OccurenceManyRegister
from server.models.http.requests.schedule_request_models import (
    ScheduleRegister,
    ScheduleUpdate,
)
from server.repositories.classroom_repository import ClassroomRepository
from server.repositories.occurrence_repository import OccurrenceRepository
from server.utils.schedule_utils import ScheduleUtils


class ScheduleRepository:
    @staticmethod
    def get_all(*, session: Session) -> list[Schedule]:
        statement = select(Schedule)
        schedules = session.exec(statement).all()
        return list(schedules)

    @staticmethod
    def get_by_id(*, id: int, session: Session) -> Schedule:
        statement = select(Schedule).where(col(Schedule.id) == id)
        schedule = session.exec(statement).one()
        return schedule

    @staticmethod
    def get_all_on_class(*, class_: Class, session: Session) -> list[Schedule]:
        statement = select(Schedule).where(Schedule.class_id == class_.id)
        schedules = list(session.exec(statement).all())
        return schedules

    @staticmethod
    def get_by_id_on_class(*, class_: Class, id: int, session: Session) -> Schedule:
        statement = (
            select(Schedule)
            .where(Schedule.class_id == class_.id)
            .where(Schedule.id == id)
        )
        schedule = session.exec(statement).one()
        return schedule

    @staticmethod
    def get_by_id_on_building(
        *, schedule_id: int, building: Building, session: Session
    ) -> Schedule:
        statement = select(Schedule).where(Schedule.id == schedule_id)

        try:
            schedule = session.exec(statement).one()
        except NoResultFound:
            raise ScheduleNotFound()

        buildings = schedule.class_.subject.buildings
        if building.id not in [building.id for building in buildings]:
            raise ScheduleNotFound()

        return schedule

    @staticmethod
    def create_with_class(
        *, class_input: Class, input: ScheduleRegister, session: Session
    ) -> Schedule:
        new_schedule = Schedule(
            start_date=input.start_date,
            end_date=input.end_date,
            recurrence=input.recurrence,
            month_week=input.month_week,
            all_day=input.all_day,
            allocated=input.allocated if input.allocated else False,
            week_day=input.week_day,
            start_time=input.start_time,
            end_time=input.end_time,
            class_id=class_input.id,
            class_=class_input,
            reservation_id=None,
            classroom_id=None,
        )
        session.add(new_schedule)
        session.commit()
        session.refresh(new_schedule)

        if input.dates and new_schedule.id:
            occurences_input = OccurenceManyRegister(
                classroom_id=None,
                schedule_id=new_schedule.id,
                start_time=input.start_time,
                end_time=input.end_time,
                dates=input.dates,
            )
            occurences = OccurrenceRepository.create_many_with_schedule(
                schedule=new_schedule, input=occurences_input, session=session
            )
            new_schedule.occurrences = occurences
            session.add(new_schedule)
            session.refresh(new_schedule)

        return new_schedule

    @staticmethod
    def create_many_with_class(
        *, university_class: Class, input: list[ScheduleRegister], session: Session
    ) -> list[Schedule]:
        return [
            ScheduleRepository.create_with_class(
                class_input=university_class, input=schedule_input, session=session
            )
            for schedule_input in input
        ]

    @staticmethod
    def update_class_schedules(
        *, class_: Class, input: list[ScheduleUpdate], session: Session
    ) -> list[Schedule]:
        old_schedules = ScheduleUtils.sort_schedules(class_.schedules)
        schedules_inputs = ScheduleUtils.sort_schedules_input(input)
        new_schedules: list[Schedule] = []
        old_size = len(old_schedules)
        new_size = len(schedules_inputs)

        range_size = min(old_size, new_size)
        for i in range(range_size):
            schedule = old_schedules[i]
            schedule_input = schedules_inputs[i]

            if ScheduleUtils.has_schedule_diff(schedule, schedules_inputs[i]):
                session.delete(schedule)
                new_schedule = ScheduleRepository.create_with_class(
                    class_input=class_, input=schedule_input, session=session
                )
                if schedule_input.allocated and schedule_input.classroom_id:
                    classroom = ClassroomRepository.get_by_id(
                        id=schedule_input.classroom_id, session=session
                    )
                    OccurrenceRepository.allocate_schedule(
                        schedule=new_schedule, classroom=classroom, session=session
                    )
                new_schedules.append(new_schedule)
            else:
                new_schedules.append(schedule)

        if old_size < new_size:
            # Add the rest of schedules
            for i in range(len(new_schedules), new_size):
                schedule_input = schedules_inputs[i]
                new_schedule = ScheduleRepository.create_with_class(
                    class_input=class_, input=schedule_input, session=session
                )
                if schedule_input.allocated and schedule_input.classroom_id:
                    classroom = ClassroomRepository.get_by_id(
                        id=schedule_input.classroom_id, session=session
                    )
                    OccurrenceRepository.allocate_schedule(
                        schedule=new_schedule, classroom=classroom, session=session
                    )
                new_schedules.append(new_schedule)

        return new_schedules

    @staticmethod
    def delete(*, id: int, session: Session) -> None:
        schedule = ScheduleRepository.get_by_id(id=id, session=session)
        session.delete(schedule)
        return


class ScheduleInvalidData(HTTPException):
    def __init__(self, schedule_info: str, data_info: str) -> None:
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            f"Schedule with {schedule_info} has invalid {data_info} value",
        )


class ScheduleNotFound(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail="Schedule not found")
