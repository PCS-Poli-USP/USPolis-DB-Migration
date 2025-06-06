from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, col, select

from server.models.database.building_db_model import Building
from server.models.database.class_db_model import Class
from server.models.database.group_db_model import Group
from server.models.database.subject_building_link import SubjectBuildingLink
from server.models.database.subject_db_model import Subject
from server.models.database.user_db_model import User
from server.models.http.requests.building_request_models import (
    BuildingRegister,
    BuildingUpdate,
)
from server.utils.must_be_int import must_be_int


class BuildingRepository:
    @staticmethod
    def get_all(*, session: Session) -> list[Building]:
        statement = select(Building)
        buildings = list(session.exec(statement).all())
        return buildings

    @staticmethod
    def get_by_id(id: int, *, session: Session) -> Building:
        statement = select(Building).where(col(Building.id) == id)
        building = session.exec(statement).first()
        if building is None:
            raise BuildingNotFound(str(id))
        return building

    @staticmethod
    def get_by_name(name: str, *, session: Session) -> Building:
        statement = select(Building).where(col(Building.name) == name)
        building = session.exec(statement).first()
        if building is None:
            raise BuildingNotFound(name)
        return building

    @staticmethod
    def get_by_ids(*, ids: list[int], session: Session) -> list[Building]:
        statement = select(Building).where(col(Building.id).in_(ids))
        buildings = list(session.exec(statement).all())
        return buildings

    @staticmethod
    def get_by_class(*, class_: Class, session: Session) -> list[Building]:
        return BuildingRepository.get_by_class_id(
            class_id=must_be_int(class_.id), session=session
        )

    @staticmethod
    def get_by_class_id(*, class_id: int, session: Session) -> list[Building]:
        statement = (
            select(Building)
            .join(SubjectBuildingLink)
            .where(col(Building.id) == SubjectBuildingLink.building_id)
            .join(Subject)
            .where(col(Subject.id) == SubjectBuildingLink.subject_id)
            .join(Class)
            .where(col(Class.id) == class_id)
        )

        try:
            buildings = session.exec(statement).all()
        except NoResultFound:
            raise BuildingNotFound(f"Classe ${class_id}")
        return list(buildings)

    @staticmethod
    def get_by_subject_id(*, subject_id: int, session: Session) -> list[Building]:
        statement = (
            select(Building)
            .join(SubjectBuildingLink)
            .where(col(SubjectBuildingLink.subject_id) == subject_id)
        )

        try:
            buildings = session.exec(statement).all()
        except NoResultFound:
            raise BuildingNotFound(f"Disciplina ${subject_id}")
        return list(buildings)

    @staticmethod
    def create(
        *, building_in: BuildingRegister, creator: User, session: Session
    ) -> Building:
        building = Building(
            name=building_in.name,
            created_by=creator,
        )
        session.add(building)
        session.flush()

        group = Group(
            name=building_in.name,
            building=building,
            users=[],
            classrooms=[],
        )  # type: ignore
        session.add(group)
        session.flush()

        building.main_group = group
        session.add(building)
        return building

    @staticmethod
    def update(*, id: int, input: BuildingUpdate, session: Session) -> Building:
        building = BuildingRepository.get_by_id(id=id, session=session)
        building.name = input.name
        session.add(building)
        return building

    @staticmethod
    def delete(*, id: int, session: Session) -> None:
        building = BuildingRepository.get_by_id(id=id, session=session)
        building.main_group = None
        session.add(building)
        session.flush()
        session.delete(building)


class BuildingNotFound(HTTPException):
    def __init__(self, building_info: str) -> None:
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            f"Prédio com {building_info} não encontrado",
        )
