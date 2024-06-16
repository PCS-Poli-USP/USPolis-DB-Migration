from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import Session, col, select

from server.deps.authenticate import BuildingDep
from server.deps.session_dep import SessionDep
from server.models.database.subject_db_model import Subject
from server.models.http.requests.subject_request_models import (
    SubjectRegister,
    SubjectUpdate,
)


class SubjectRepository:
    @staticmethod
    def get_all(*, session: Session) -> list[Subject]:
        statement = select(Subject)
        subjects = session.exec(statement).all()
        return list(subjects)

    @staticmethod
    def get_by_id(*, id: int, session: Session) -> Subject:
        statement = select(Subject).where(col(Subject.id) == id)
        subject = session.exec(statement).first()
        if subject is None:
            raise SubjectNotExists(str(id))
        return subject

    @staticmethod
    def get_by_ids(*, ids: list[int], session: Session) -> list[Subject]:
        statement = select(Subject).where(col(Subject.id).in_(ids))
        subjects = session.exec(statement).all()
        return list(subjects)

    @staticmethod
    def get_by_code(*, code: str, session: Session) -> Subject:
        statement = select(Subject).where(Subject.code == code)
        subject = session.exec(statement).one()
        if subject is None:
            raise SubjectNotExists(code)
        return subject

    @staticmethod
    def create(*, input: SubjectRegister, session: Session) -> Subject:
        new_subject = Subject(
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
    def crawler_create(
        subject: Subject, session: SessionDep, building: BuildingDep
    ) -> Subject:
        try:
            session.add(subject)
            session.commit()
        except IntegrityError:
            # subject_code already exists
            # add building to existing subject
            # it is NOT updating schedule's info and relations!
            subject = SubjectRepository.get_by_code(code=subject.code, session=session)
            if subject.buildings is None:
                subject.buildings = [building]
            elif (
                building not in subject.buildings
            ):  # dont know if it works... its comparing objects
                subject.buildings.append(building)
            else:
                return subject
            session.add(subject)
            session.commit()
        session.refresh(subject)
        return subject

    @staticmethod
    def update(*, id: int, input: SubjectUpdate, session: Session) -> Subject:
        subject = SubjectRepository.get_by_id(id=id, session=session)
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


class SubjectNotExists(HTTPException):
    def __init__(self, subject_info: str) -> None:
        super().__init__(
            status.HTTP_404_NOT_FOUND, f"Subject {subject_info} not exists"
        )
