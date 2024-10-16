from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound
from sqlmodel import col, select, Session

from server.models.database.building_db_model import Building
from server.models.database.classroom_db_model import Classroom
from server.models.database.reservation_db_model import Reservation
from server.models.database.user_db_model import User
from server.models.http.requests.reservation_request_models import (
    ReservationRegister,
    ReservationUpdate,
)
from server.repositories.schedule_repository import ScheduleRepository
from server.utils.must_be_int import must_be_int


class ReservationRepository:
    @staticmethod
    def get_all(*, session: Session) -> list[Reservation]:
        statement = select(Reservation)
        reservations = session.exec(statement).all()
        return list(reservations)

    @staticmethod
    def get_all_on_buildings(
        *, building_ids: list[int], session: Session
    ) -> list[Reservation]:
        statement = (
            select(Reservation)
            .join(Classroom)
            .join(Building)
            .where(col(Building.id).in_(building_ids))
        )
        reservations = list(session.exec(statement).all())
        return reservations

    @staticmethod
    def get_by_id(*, id: int, session: Session) -> Reservation:
        statement = select(Reservation).where(col(Reservation.id) == id)
        reservation = session.exec(statement).one()
        return reservation

    @staticmethod
    def get_by_id_on_buildings(
        *, id: int, building_ids: list[int], session: Session
    ) -> Reservation:
        statement = (
            select(Reservation)
            .join(Classroom)
            .join(Building)
            .where(col(Building.id).in_(building_ids))
            .where(col(Reservation.id) == id)
        )
        try:
            reservation = session.exec(statement).one()
        except NoResultFound:
            raise ReservationNotFound(id)
        return reservation

    @staticmethod
    def create(
        *,
        creator: User,
        input: ReservationRegister,
        classroom: Classroom,
        session: Session,
    ) -> Reservation:
        reservation = Reservation(
            name=input.name,
            type=input.type,
            description=input.description,
            updated_at=datetime.now(),
            classroom=classroom,
            created_by_id=must_be_int(creator.id),
            created_by=creator,
        )
        schedule = ScheduleRepository.create_with_reservation(
            reservation=reservation,
            input=input.schedule_data,
            classroom=classroom,
            session=session,
        )
        reservation.schedule = schedule
        session.add(reservation)
        return reservation

    @staticmethod
    def update_on_buildings(
        *,
        id: int,
        building_ids: list[int],
        input: ReservationUpdate,
        classroom: Classroom,
        session: Session,
    ) -> Reservation:
        reservation = ReservationRepository.get_by_id_on_buildings(
            id=id, building_ids=building_ids, session=session
        )
        reservation.name = input.name
        reservation.type = input.type
        reservation.description = input.description
        reservation.classroom = classroom

        schedule = ScheduleRepository.update_reservation_schedule(
            reservation=reservation,
            input=input.schedule_data,
            classroom=classroom,
            session=session,
        )
        session.add(reservation)
        return reservation

    @staticmethod
    def delete_on_buildings(
        *, id: int, building_ids: list[int], session: Session
    ) -> None:
        reservation = ReservationRepository.get_by_id_on_buildings(
            id=id, building_ids=building_ids, session=session
        )
        session.delete(reservation)


class ReservationNotFound(HTTPException):
    def __init__(self, id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Classroom with id {id} not found",
        )
