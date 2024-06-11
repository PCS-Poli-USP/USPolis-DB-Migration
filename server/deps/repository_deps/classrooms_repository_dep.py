from typing import Annotated

from fastapi import Depends

from server.deps.authenticate import BuildingDep, UserDep
from server.deps.session_dep import SessionDep
from server.models.database.classroom_db_model import Classroom
from server.models.http.requests.classroom_request_models import ClassroomRegister
from server.repositories.classrooms_repository import ClassroomRepository


class ClassroomRepositoryAdapter:
    def __init__(self, building: BuildingDep, session: SessionDep, user: UserDep):
        self.building = building
        self.session = session
        self.user = user

    def get_all(self) -> list[Classroom]:
        return ClassroomRepository.get_all_on_building(
            building=self.building, session=self.session
        )

    def get_by_id(self, id: int) -> Classroom:
        return ClassroomRepository.get_by_id_on_building(
            building=self.building, id=id, session=self.session
        )

    def create(
        self,
        classroom: ClassroomRegister,
    ) -> Classroom:
        return ClassroomRepository.create(
            building=self.building,
            classroom=classroom,
            creator=self.user,
            session=self.session,
        )

    def update(
        self,
        id: int,
        classroom: ClassroomRegister,
    ) -> Classroom:
        return ClassroomRepository.update_on_building(
            id=id,
            building=self.building,
            classroom_in=classroom,
            session=self.session,
        )

    def delete(self, id: int) -> None:
        ClassroomRepository.delete_on_building(
            id=id, building=self.building, session=self.session
        )


ClassroomRepositoryDep = Annotated[ClassroomRepositoryAdapter, Depends()]
