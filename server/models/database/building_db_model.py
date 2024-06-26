from datetime import datetime
from typing import Annotated, Self

from beanie import Document, Indexed, Link
from fastapi import HTTPException, status


class Building(Document):
    name: Annotated[str, Indexed(unique=True)]
    created_by: Link["User"]  # type: ignore  # noqa: F821
    updated_at: datetime

    class Settings:
        name = "buildings"

    @classmethod
    async def by_name(cls, name: str) -> Self:
        building = await cls.find_one(cls.name == name)
        if building is None:
            raise BuildingNotFound(name)
        return building

    @classmethod
    async def by_id(cls, id: str) -> Self:
        building = await cls.get(id)
        if building is None:
            raise BuildingNotFound(id)
        return building

    @classmethod
    async def check_name_exits(cls, name: str) -> bool:
        return await cls.find_one(cls.name == name) is not None

    @classmethod
    async def check_name_is_valid(cls, building_id: str, name: str) -> bool:
        """Check if the name of building is not used in other building"""
        current = await cls.find_one(cls.name == name)
        if current is None:
            return True
        return str(current.id) == building_id

    @classmethod
    async def by_ids(cls, ids: list[str]) -> list["Building"]:
        async def get_building_by_id(id: str) -> Building:
            building = await Building.get(id)
            if not building:
                raise BuildingNotFound(id)
            return building

        return [await get_building_by_id(id) for id in ids]


class BuildingNotFound(HTTPException):
    def __init__(self, building_info: str) -> None:
        super().__init__(
            status.HTTP_404_NOT_FOUND, f"Building {building_info} not found"
        )
