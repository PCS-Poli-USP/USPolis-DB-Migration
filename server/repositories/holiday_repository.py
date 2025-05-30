from datetime import datetime

from fastapi import HTTPException, status
from sqlmodel import col, select, Session
from sqlalchemy.exc import NoResultFound

from server.models.database.holiday_db_model import Holiday
from server.models.database.user_db_model import User
from server.models.http.requests.holiday_request_models import (
    HolidayManyRegister,
    HolidayRegister,
    HolidayUpdate,
)
from server.repositories.holiday_category_repository import HolidayCategoryRepository
from server.utils.brazil_datetime import BrazilDatetime
from server.utils.must_be_int import must_be_int


class HolidayRepository:
    @staticmethod
    def get_all(*, session: Session) -> list[Holiday]:
        statement = select(Holiday)
        holidays = session.exec(statement).all()
        return list(holidays)

    @staticmethod
    def get_by_id(*, id: int, session: Session) -> Holiday:
        statement = select(Holiday).where(col(Holiday.id) == id)
        try:
            holiday = session.exec(statement).one()
        except NoResultFound:
            raise HolidayNotFound(f"id {id}")
        return holiday

    @staticmethod
    def check_date_is_valid(
        *, category_id: int, date: datetime, session: Session
    ) -> bool:
        statement = (
            select(Holiday)
            .where(col(Holiday.category_id) == category_id)
            .where(col(Holiday.date) == date)
        )
        result = session.exec(statement).first()
        return result is None

    @staticmethod
    def create(*, creator: User, input: HolidayRegister, session: Session) -> Holiday:
        category = HolidayCategoryRepository.get_by_id(
            id=input.category_id, session=session
        )
        if not creator.is_admin and creator.id != category.created_by_id:
            raise HolidayOperationNotAllowed("create", input.date.strftime("%d/%m/%Y"))

        new_holiday = Holiday(
            name=input.name,
            date=input.date,
            category_id=input.category_id,
            category=category,
            updated_at=BrazilDatetime.now_utc(),
            created_by_id=must_be_int(creator.id),
            created_by=creator,
        )
        session.add(new_holiday)
        session.commit()
        session.refresh(new_holiday)
        return new_holiday

    @staticmethod
    def create_many(
        *, creator: User, input: HolidayManyRegister, session: Session
    ) -> list[Holiday]:
        dates = input.dates
        category_id = input.category_id
        name = input.name
        holidays = [
            HolidayRepository.create(
                creator=creator,
                input=HolidayRegister(name=name, category_id=category_id, date=date),
                session=session,
            )
            for date in dates
        ]
        return holidays

    @staticmethod
    def update(
        *, id: int, input: HolidayUpdate, user: User, session: Session
    ) -> Holiday:
        holiday = HolidayRepository.get_by_id(id=id, session=session)
        if not user.is_admin and holiday.created_by_id != user.id:
            raise HolidayOperationNotAllowed(
                "atualizar", input.date.strftime("%d/%m/%Y")
            )
        holiday.name = input.name
        holiday.date = input.date
        holiday.updated_at = BrazilDatetime.now_utc()
        session.add(holiday)
        session.commit()
        return holiday

    @staticmethod
    def delete(*, id: int, user: User, session: Session) -> None:
        holiday = HolidayRepository.get_by_id(id=id, session=session)
        if not user.is_admin and holiday.created_by_id != user.id:
            raise HolidayOperationNotAllowed(
                "remover", holiday.date.strftime("%d/%m/%Y")
            )
        session.delete(holiday)
        session.commit()


class HolidayNotFound(HTTPException):
    def __init__(self, holiday_info: str) -> None:
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            f"Feriado {holiday_info} não encontrado",
        )


class HolidayInCategoryAlreadyExists(HTTPException):
    def __init__(self, holiday_info: str, category_info: str) -> None:
        super().__init__(
            status.HTTP_409_CONFLICT,
            f"Feriado {holiday_info} na Categoria {category_info} já existe",
        )


class HolidayOperationNotAllowed(HTTPException):
    def __init__(self, operation: str, holiday_info: str) -> None:
        super().__init__(
            status.HTTP_403_FORBIDDEN,
            f"Apenas o criado pode {operation} o Feriado {holiday_info}",
        )
