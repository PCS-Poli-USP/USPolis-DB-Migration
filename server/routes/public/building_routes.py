from fastapi import APIRouter

from server.deps.session_dep import SessionDep
from server.models.database.building_db_model import Building
from server.models.http.responses.building_response_models import BuildingResponse
from server.repositories.buildings_repository import BuildingRepository

router = APIRouter(prefix="/buildings", tags=["Buildings"])


@router.get("", response_model_by_alias=False)
async def get_all_buildings(session: SessionDep) -> list[BuildingResponse]:
    """Get all buildings"""
    buildings = BuildingRepository.get_all(session=session)
    return BuildingResponse.from_building_list(buildings)


@router.get("/{building_id}", response_model_by_alias=False)
async def get_building(building_id: int, session: SessionDep) -> BuildingResponse:
    """Get a building"""
    building: Building = BuildingRepository.get_by_id(building_id, session=session)
    return BuildingResponse.from_building(building)
