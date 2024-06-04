from pydantic import BaseModel

from server.models.database.holiday_category_db_model import HolidayCategory
from server.models.database.holiday_db_model import Holiday


class HolidayCategoryResponse(BaseModel):
    id: int
    name: str
    created_by: str
    holidays: list[Holiday]

    @classmethod
    def from_holiday_category(
        cls, holiday_category: HolidayCategory
    ) -> "HolidayCategoryResponse":
        if holiday_category.id is None:
            raise ValueError(
                "HolidayCategory ID is None, try refreshing the session if it is newly created"
            )
        return cls(
            id=holiday_category.id,
            name=holiday_category.name,
            created_by=holiday_category.created_by.name,
            holidays=holiday_category.holidays,
        )

    @classmethod
    def from_holiday_category_list(
        cls, holidays_categories: list[HolidayCategory]
    ) -> list["HolidayCategoryResponse"]:
        return [
            cls.from_holiday_category(holiday_category)
            for holiday_category in holidays_categories
        ]
