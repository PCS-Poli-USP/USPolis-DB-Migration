from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, col, select

from server.deps.authenticate import BuildingDep
from server.models.database.subject_building_link import SubjectBuildingLink
from server.models.database.subject_db_model import Subject
from server.models.http.requests.subject_request_models import (
    SubjectRegister,
    SubjectUpdate,
)
from server.repositories.building_repository import BuildingRepository
from server.repositories.calendar_repository import CalendarRepository
from server.services.jupiter_crawler.crawler import JupiterCrawler
from server.utils.enums.subject_type import SubjectType


class SubjectRepository:
    @staticmethod
    def get_all(*, session: Session) -> list[Subject]:
        statement = select(Subject)
        subjects = session.exec(statement).all()
        return list(subjects)

    @staticmethod
    def get_all_on_buildings(
        *, building_ids: list[int], session: Session
    ) -> list[Subject]:
        statement = (
            select(Subject)
            .join(SubjectBuildingLink)
            .where(col(SubjectBuildingLink.building_id).in_(building_ids))
        )
        subjects = session.exec(statement).all()
        return list(subjects)

    @staticmethod
    def get_by_id(*, id: int, session: Session) -> Subject:
        statement = select(Subject).where(col(Subject.id) == id)
        try:
            subject = session.exec(statement).one()
            return subject
        except NoResultFound:
            raise SubjectNotFound()

    @staticmethod
    def get_by_id_on_buildings(
        *, id: int, building_ids: list[int], session: Session
    ) -> Subject:
        statement = (
            select(Subject)
            .join(SubjectBuildingLink)
            .where(col(SubjectBuildingLink.building_id).in_(building_ids))
            .where(col(Subject.id) == id)
        )
        try:
            subject = session.exec(statement).one()
            return subject
        except NoResultFound:
            raise SubjectNotFound()

    @staticmethod
    def get_by_ids(*, ids: list[int], session: Session) -> list[Subject]:
        statement = select(Subject).where(col(Subject.id).in_(ids))
        subjects = session.exec(statement).all()
        return list(subjects)

    @staticmethod
    def get_by_code(*, code: str, session: Session) -> Subject:
        statement = select(Subject).where(Subject.code == code)
        try:
            subject = session.exec(statement).one()
            return subject
        except NoResultFound:
            raise SubjectNotFound()

    @staticmethod
    def create(*, input: SubjectRegister, session: Session) -> Subject:
        new_subject = Subject(
            buildings=BuildingRepository.get_by_ids(
                ids=input.building_ids, session=session
            ),
            name=input.name,
            code=input.code,
            professors=input.professors,
            type=input.type,
            class_credit=input.class_credit,
            work_credit=input.work_credit,
            activation=input.activation,
            deactivation=input.desactivation,
        )
        session.add(new_subject)
        session.commit()
        session.refresh(new_subject)
        return new_subject

    @staticmethod
    async def crawler_create_many(
        subjects_codes: list[str],
        calendar_ids: list[int],
        session: Session,
        building: BuildingDep,
    ) -> list[Subject]:
        calendars = CalendarRepository.get_by_ids(ids=calendar_ids, session=session)
        result: list[Subject] = []
        errors: list[str] = []
        for subject_code in subjects_codes:
            subject = await JupiterCrawler.crawl_subject_static(subject_code, calendars)
            subject.buildings = [building]
            session.add(subject)
            result.append(subject)
            try:
                session.commit()
            except:
                session.reset()
                errors.append(subject_code)
        if len(errors) > 0:
            raise SubjectCreationError(subjects=errors)
        for subject in result:
            session.refresh(subject)
        return result

    @staticmethod
    def update(*, id: int, input: SubjectUpdate, session: Session) -> Subject:
        subject = SubjectRepository.get_by_id(id=id, session=session)
        subject.buildings = BuildingRepository.get_by_ids(
            ids=input.building_ids, session=session
        )
        subject.name = input.name
        subject.code = input.code
        subject.professors = input.professors
        subject.type = input.type
        subject.class_credit = input.class_credit
        subject.work_credit = input.work_credit
        subject.activation = input.activation
        subject.deactivation = input.desactivation
        session.add(subject)
        session.commit()
        return subject

    @staticmethod
    def delete(*, id: int, session: Session) -> None:
        subject = SubjectRepository.get_by_id(id=id, session=session)
        session.delete(subject)
        session.commit()

    @staticmethod
    def create_general_forum(*, id: int, name: str, session: Session) -> Subject:
        new_subject = Subject(
            id=id,
            name=name,
            code="",
            professors=[],
            type=SubjectType.OTHER,
            work_credit=0,
            class_credit=0,
            activation=date.today(),
        )
        session.add(new_subject)
        session.commit()
        session.refresh(new_subject)
        return new_subject

    @staticmethod
    def get_by_name(*, name: str, session: Session) -> Subject:
        statement = select(Subject).where(Subject.name == name)
        try:
            subject = session.exec(statement).one()
            return subject
        except NoResultFound:
            raise SubjectNotFound()


class SubjectNotFound(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, f"Subject not found")


class SubjectNotExists(HTTPException):
    def __init__(self, subject_info: str) -> None:
        super().__init__(
            status.HTTP_404_NOT_FOUND, f"Subject {subject_info} not exists"
        )


class SubjectCreationError(HTTPException):
    def __init__(self, subjects: list) -> None:
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            f"Erro ao criar as seguintes disciplinas: {", ".join(subjects)}",
        )
