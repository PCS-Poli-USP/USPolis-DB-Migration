from fastapi import HTTPException, status
from sqlmodel import Session, col, select
from server.models.database.calendar_db_model import Calendar
from server.models.database.user_db_model import User
from server.models.http.requests.calendar_request_models import (
    CalendarRegister,
    CalendarUpdate,
)
from server.repositories.holiday_category_repository import HolidayCategoryRepository


class CalendarRepository:
    @staticmethod
    def get_all(*, session: Session) -> list[Calendar]:
        statement = select(Calendar)
        calendars = session.exec(statement).all()
        return list(calendars)

    @staticmethod
    def get_by_id(*, id: int, session: Session) -> Calendar:
        statement = select(Calendar).where(col(Calendar.id) == id)
        calendar = session.exec(statement).first()
        if calendar is None:
            raise CalendarNotExists(str(id))
        return calendar

    @staticmethod
    def get_by_name(*, name: str, session: Session) -> Calendar:
        statement = select(Calendar).where(col(Calendar.name) == name)
        calendar = session.exec(statement).first()
        if calendar is None:
            raise CalendarNotExists(name)
        return calendar

    @staticmethod
    def create(*, creator: User, input: CalendarRegister, session: Session) -> Calendar:
        categories = HolidayCategoryRepository.get_by_ids(
            ids=input.categories_ids, session=session
        )
        new_calendar = Calendar(
            name=input.name,
            categories=categories,
            created_by=creator,
        )
        session.add(new_calendar)
        session.commit()
        session.refresh(new_calendar)
        return new_calendar

    @staticmethod
    def update(
        *, id: int, input: CalendarUpdate, user: User, session: Session
    ) -> Calendar:
        calendar = CalendarRepository.get_by_id(id=id, session=session)
        if calendar.created_by_id != user.id:
            raise CalendarOperationNotAllowed("Update", input.name)
        calendar.name = input.name
        if input.categories_ids:
            calendar.categories = HolidayCategoryRepository.get_by_ids(
                ids=input.categories_ids, session=session
            )
        session.add(calendar)
        session.commit()
        return calendar

    @staticmethod
    def delete(*, id: int, user: User, session: Session) -> None:
        calendar = CalendarRepository.get_by_id(id=id, session=session)
        if calendar.created_by_id != user.id:
            raise CalendarOperationNotAllowed("Delete", calendar.name)
        session.delete(calendar)
        session.commit()


class CalendarNotExists(HTTPException):
    def __init__(self, calendar_info: str) -> None:
        super().__init__(
            status.HTTP_404_NOT_FOUND, f"Calendar {calendar_info} not exists"
        )


class CalendarOperationNotAllowed(HTTPException):
    def __init__(self, operation: str, calendar_info: str) -> None:
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            f"Only the creator is Allowed to {operation} Calendar {calendar_info}",
        )