from datetime import datetime
from pydantic import BaseModel

from server.models.database.reservation_db_model import Reservation
from server.models.http.exceptions.responses_exceptions import UnfetchDataError
from server.models.http.responses.classroom_solicitation_response_models import (
    ClassroomSolicitationResponse,
)
from server.models.http.responses.schedule_response_models import (
    ScheduleResponse,
    ScheduleFullResponse,
)
from server.utils.enums.reservation_type import ReservationType
from server.utils.must_be_int import must_be_int


class ReservationResponseBase(BaseModel):
    id: int
    title: str
    type: ReservationType
    reason: str | None
    updated_at: datetime

    building_id: int
    building_name: str

    classroom_id: int
    classroom_name: str

    schedule_id: int

    created_by_id: int
    created_by: str

    solicitation: ClassroomSolicitationResponse | None


class ReservationResponse(ReservationResponseBase):
    schedule: ScheduleResponse

    @classmethod
    def from_reservation(cls, reservation: Reservation) -> "ReservationResponse":
        if reservation.classroom.building is None:
            raise UnfetchDataError("Classroom", "Building")
        return cls(
            id=must_be_int(reservation.id),
            title=reservation.title,
            type=reservation.type,
            reason=reservation.reason,
            updated_at=reservation.updated_at,
            building_id=must_be_int(reservation.classroom.building_id),
            building_name=reservation.classroom.building.name,
            classroom_id=must_be_int(reservation.classroom_id),
            classroom_name=reservation.classroom.name,
            schedule_id=must_be_int(reservation.schedule.id),
            schedule=ScheduleResponse.from_schedule(reservation.schedule),
            created_by_id=must_be_int(reservation.created_by_id),
            created_by=reservation.created_by.name,
            solicitation=ClassroomSolicitationResponse.from_solicitation(
                reservation.solicitation
            )
            if reservation.solicitation
            else None,
        )

    @classmethod
    def from_reservation_list(
        cls, reservations: list[Reservation]
    ) -> list["ReservationResponse"]:
        return [cls.from_reservation(reservation) for reservation in reservations]


class ReservationFullResponse(ReservationResponseBase):
    schedule: ScheduleFullResponse

    @classmethod
    def from_reservation(cls, reservation: Reservation) -> "ReservationFullResponse":
        if reservation.classroom.building is None:
            raise UnfetchDataError("Classroom", "Building")
        return cls(
            id=must_be_int(reservation.id),
            title=reservation.title,
            type=reservation.type,
            reason=reservation.reason,
            updated_at=reservation.updated_at,
            building_id=must_be_int(reservation.classroom.building_id),
            building_name=reservation.classroom.building.name,
            classroom_id=must_be_int(reservation.classroom_id),
            classroom_name=reservation.classroom.name,
            schedule_id=must_be_int(reservation.schedule.id),
            schedule=ScheduleFullResponse.from_schedule(reservation.schedule),
            created_by_id=must_be_int(reservation.created_by_id),
            created_by=reservation.created_by.name,
            solicitation=ClassroomSolicitationResponse.from_solicitation(
                reservation.solicitation
            )
            if reservation.solicitation
            else None,
        )

    @classmethod
    def from_reservation_list(
        cls, reservations: list[Reservation]
    ) -> list["ReservationFullResponse"]:
        return [cls.from_reservation(reservation) for reservation in reservations]
