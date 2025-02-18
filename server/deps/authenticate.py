from typing import Annotated

from fastapi import Depends, Header, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from server.deps.session_dep import SessionDep
from server.models.database.building_db_model import Building
from server.models.database.user_db_model import User
from server.repositories.building_repository import BuildingRepository
from server.repositories.user_repository import UserRepository
from server.services.auth.auth_user_info import AuthUserInfo
from server.services.auth.authentication_client import (
    AuthenticationClient,
)
from server.models.http.requests.user_request_models import UserRegister
from sqlalchemy.exc import NoResultFound

security = HTTPBearer()


def google_authenticate(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> AuthUserInfo:
    access_token = credentials.credentials
    return AuthenticationClient.get_user_info(access_token)


def authenticate(
    request: Request,
    user_info: Annotated[AuthUserInfo, Depends(google_authenticate)],
    session: SessionDep,
) -> User:
    try:
        user: User = UserRepository.get_by_email(email=user_info.email, session=session)
    except NoResultFound:
        user = UserRepository.create(
            user_in=UserRegister(
                email=user_info.email,
                name=user_info.name,
                building_ids=None,
                is_admin=False,
            ),
            creator=None,
            session=session,
        )
    request.state.current_user = user
    return user


def admin_authenticate(user: Annotated[User, Depends(authenticate)]) -> None:
    if not user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "User must be admin")


# -- permission authentications :


def building_authenticate(
    user: Annotated[User, Depends(authenticate)],
    session: SessionDep,
    building_id: Annotated[int, Header()],
) -> Building:
    building = BuildingRepository.get_by_id(id=building_id, session=session)
    if user.is_admin:
        return building
    if user.buildings is None or building not in user.buildings:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "User must have access to building"
        )
    return building


# exports:
GoogleAuthenticate = Annotated[AuthUserInfo, Depends(google_authenticate)]
UserDep = Annotated[User, Depends(authenticate)]
BuildingDep = Annotated[Building, Depends(building_authenticate)]
