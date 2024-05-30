from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

from server.models.database.calendar_holiday_category_link import CalendarHolidayCategoryLink

if TYPE_CHECKING:
    from server.models.database.user_db_model import User
    from server.models.database.holiday_category_db_model import HolidayCategory  # noqa: F401


class Calendar(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

    categories: list["HolidayCategory"] = Relationship(
        back_populates="calendars", link_model=CalendarHolidayCategoryLink)

    created_by_id: int | None = Field(default=None, foreign_key="user.id")
    created_by: "User" = Relationship(back_populates="calendars")