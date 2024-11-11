from pydantic import BaseModel

from server.models.http.requests.schedule_request_models import (
    ScheduleRegister,
    ScheduleUpdate,
)
from server.utils.enums.reservation_type import ReservationType


class ReservationBase(BaseModel):
    title: str
    type: ReservationType
    reason: str | None = None
    classroom_id: int


class ReservationRegister(ReservationBase):
    schedule_data: ScheduleRegister


class ReservationUpdate(ReservationBase):
    schedule_data: ScheduleUpdate
