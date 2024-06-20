from datetime import date as datetime_date
from datetime import time
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from server.models.database.classroom_db_model import Classroom
    from server.models.database.schedule_db_model import Schedule


class Occurrence(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    start_time: time = Field(nullable=False)
    end_time: time = Field(nullable=False)
    date: datetime_date = Field()

    # TODO: pensar se não é ruim que tenham ocorrencias sem classroom
    classroom_id: int | None = Field(
        default=None, foreign_key="classroom.id", nullable=True
    )
    classroom: Optional["Classroom"] = Relationship(back_populates="occurrences")

    schedule_id: int | None = Field(default=None, index=True, foreign_key="schedule.id")
    schedule: "Schedule" = Relationship(back_populates="occurrences")
