from fastapi import APIRouter, Body

from server.deps.owned_building_ids import OwnedBuildingIdsDep
from server.deps.session_dep import SessionDep
from server.models.http.responses.classroom_solicitation_response_models import (
    ClassroomSolicitationResponse,
)
from server.repositories.classroom_solicitation_repository import (
    ClassroomSolicitationRepository,
)

embed = Body(..., embed=True)

router = APIRouter(prefix="/solicitations/classroom", tags=["Solicitations"])


@router.get("")
def get_classroom_solicitations(
    building_ids: OwnedBuildingIdsDep, session: SessionDep
) -> list[ClassroomSolicitationResponse]:
    solicitations = ClassroomSolicitationRepository.get_by_id_on_buildings(
        building_ids=building_ids, session=session
    )
    return ClassroomSolicitationResponse.from_solicitation_list(solicitations)


@router.put("/approve/{solicitation_id}")
def aprove_classroom_solicitation(
    solicitation_id: int, session: SessionDep
) -> ClassroomSolicitationResponse:
    """Aprove a class reservation solicitation"""
    solicitation = ClassroomSolicitationRepository.approve(
        id=solicitation_id, session=session
    )
    session.commit()
    return ClassroomSolicitationResponse.from_solicitation(solicitation)


@router.put("/deny/{solicitation_id}")
def deny_classroom_solicitation(
    solicitation_id: int, session: SessionDep
) -> ClassroomSolicitationResponse:
    """Deny a class reservation solicitation"""
    solicitation = ClassroomSolicitationRepository.deny(
        id=solicitation_id, session=session
    )
    session.commit()
    return ClassroomSolicitationResponse.from_solicitation(solicitation)
