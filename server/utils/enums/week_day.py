from enum import Enum


class WeekDay(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    @classmethod
    def from_str(cls, day_str: str) -> "WeekDay":
        mapping = {
            "seg": cls.MONDAY,
            "ter": cls.TUESDAY,
            "qua": cls.WEDNESDAY,
            "qui": cls.THURSDAY,
            "sex": cls.FRIDAY,
            "sab": cls.SATURDAY,
            "dom": cls.SUNDAY,
        }
        result: WeekDay | None = mapping.get(day_str.lower())
        if result is None:
            raise NoSuchWeekDay(
                f"No such week day: {day_str}. Valid week days: {mapping.keys()}"
            )
        return result


class NoSuchWeekDay(Exception):
    pass
