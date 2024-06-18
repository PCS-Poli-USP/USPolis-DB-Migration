from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from server.models.database.classroom_db_model import Classroom
    from server.models.database.schedule_db_model import Schedule


class Occurrence(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    start_time: str = Field(nullable=False)
    end_time: str = Field(nullable=False)
    date: datetime = Field()

    classroom_id: int | None = Field(default=None, foreign_key="classroom.id")
    classroom: Optional["Classroom"] = Relationship(back_populates="occurrences")
    schedule_id: int | None = Field(
        default=None, index=True, foreign_key="schedule.id", nullable=False
    )
    schedule: "Schedule" = Relationship(back_populates="occurrences")
