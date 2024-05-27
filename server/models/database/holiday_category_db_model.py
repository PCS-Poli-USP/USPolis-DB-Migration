from sqlmodel import SQLModel, Field, Relationship

from server.models.database.user_db_model import User
from server.models.database.holiday_db_model import Holiday


class HolidayCategory(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

    created_by_id: int | None = Field(
        foreign_key="user.id", default=None, nullable=False
    )
    created_by: User = Relationship()

    holidays: list["Holiday"] = Relationship(back_populates="category")
