from datetime import datetime
from math import floor
from pydantic import BaseModel

from server.models.database.classroom_db_model import Classroom
from server.models.http.exceptions.responses_exceptions import UnfetchDataError


class ClassroomResponseBase(BaseModel):
    id: int
    name: str
    capacity: int
    floor: int
    ignore_to_allocate: bool
    accessibility: bool
    projector: bool
    air_conditioning: bool
    updated_at: datetime


class ClassroomResponse(ClassroomResponseBase):
    created_by_id: int
    created_by: str
    building_id: int
    building: str

    @classmethod
    def from_classroom(cls, classroom: Classroom) -> "ClassroomResponse":
        if classroom.id is None:
            raise UnfetchDataError("Classroom", "ID")
        if classroom.created_by_id is None:
            raise UnfetchDataError("Classroom", "created_by_id")
        if classroom.building_id is None:
            raise UnfetchDataError("Classroom", "building_id")
        return cls(
            id=classroom.id,
            name=classroom.name,
            capacity=classroom.capacity,
            floor=classroom.floor,
            ignore_to_allocate=classroom.ignore_to_allocate,
            accessibility=classroom.accessibility,
            projector=classroom.projector,
            air_conditioning=classroom.air_conditioning,
            updated_at=classroom.updated_at,
            created_by_id=classroom.created_by_id,
            created_by=classroom.created_by.name,
            building_id=classroom.building_id,
            building=classroom.building.name,
        )

    @classmethod
    def from_classroom_list(
        cls, classrooms: list[Classroom]
    ) -> list["ClassroomResponse"]:
        return [cls.from_classroom(classroom) for classroom in classrooms]