from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.dialects import postgresql
from sqlmodel import Column, Enum, Field, Relationship

from server.models.database.base_db_model import BaseModel
from server.models.database.subject_building_link import SubjectBuildingLink
from server.utils.enums.subject_type import SubjectType

if TYPE_CHECKING:
    from server.models.database.building_db_model import Building
    from server.models.database.class_db_model import Class
    from server.models.database.forum_db_model import ForumPost


class Subject(BaseModel, table=True):
    name: str = Field(nullable=False)
    code: str = Field(index=True, unique=True, nullable=False)
    professors: list[str] = Field(
        sa_column=Column(postgresql.ARRAY(String()), nullable=False)
    )
    type: SubjectType = Field(sa_column=Column(Enum(SubjectType), nullable=False))
    class_credit: int = Field(nullable=False)
    work_credit: int = Field(nullable=False)

    buildings: list["Building"] = Relationship(
        back_populates="subjects", link_model=SubjectBuildingLink
    )
    classes: list["Class"] = Relationship(
        back_populates="subject", sa_relationship_kwargs={"cascade": "all, delete"}
    )

    forum: "ForumPost" = Relationship(sa_relationship_kwargs={"cascade": "all, delete"})
