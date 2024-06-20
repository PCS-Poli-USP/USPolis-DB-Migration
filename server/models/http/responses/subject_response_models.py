from datetime import date

from pydantic import BaseModel

from server.models.database.class_db_model import Class
from server.models.database.subject_db_model import Subject
from server.models.http.exceptions.responses_exceptions import UnfetchDataError
from server.models.http.responses.building_response_models import BuildingResponse
from server.utils.enums.subject_type import SubjectType


class SubjectResponse(BaseModel):
    id: int
    building_ids: list[int]
    buildings: list[BuildingResponse]
    classes: list[Class]
    code: str
    name: str
    professors: list[str]
    type: SubjectType
    class_credit: int
    work_credit: int
    activation: date
    desactivation: date | None = None

    @classmethod
    def from_subject(cls, subject: Subject) -> "SubjectResponse":
        if subject.id is None:
            raise UnfetchDataError("Subject", "ID")
        return cls(
            id=subject.id,
            professors=subject.professors,
            building_ids=[
                building.id for building in subject.buildings if (building.id)
            ],
            buildings=[
                BuildingResponse.from_building(building)
                for building in subject.buildings
            ],
            classes=subject.classes,
            code=subject.code,
            name=subject.name,
            type=subject.type,
            class_credit=subject.class_credit,
            work_credit=subject.work_credit,
            activation=subject.activation,
            desactivation=subject.deactivation if subject.deactivation else None,
        )

    @classmethod
    def from_subject_list(cls, subjects: list[Subject]) -> list["SubjectResponse"]:
        return [cls.from_subject(subject) for subject in subjects]
