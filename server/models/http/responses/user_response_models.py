from datetime import datetime

from pydantic import BaseModel

from server.models.database.user_db_model import User
from server.models.http.responses.building_response_models import BuildingResponse
from server.models.http.responses.classroom_solicitation_response_models import (
    ClassroomSolicitationResponse,
)
from server.utils.must_be_int import must_be_int


class UserResponse(BaseModel):
    id: int
    email: str
    is_admin: bool
    name: str
    created_by: str | None = None
    buildings: list[BuildingResponse] | None = None
    solicitations: list[ClassroomSolicitationResponse]
    updated_at: datetime
    last_visited: datetime

    @classmethod
    def from_user(cls, user: User) -> "UserResponse":
        return cls(
            id=must_be_int(user.id),
            email=user.email,
            is_admin=user.is_admin,
            name=user.name,
            created_by=user.created_by.name if user.created_by else None,
            buildings=[
                BuildingResponse.from_building(building) for building in user.buildings
            ]
            if user.buildings
            else None,
            solicitations=ClassroomSolicitationResponse.from_solicitation_list(
                user.solicitations
            ),
            updated_at=user.updated_at,
            last_visited=user.last_visited,
        )

    @classmethod
    def from_user_list(cls, users: list[User]) -> list["UserResponse"]:
        return [cls.from_user(user) for user in users]
