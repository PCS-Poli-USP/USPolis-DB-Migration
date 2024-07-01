from fastapi import HTTPException

from server.models.database.building_db_model import Building
from server.models.database.user_db_model import User


def building_permission_checker(
    user: User, building: int | Building | list[int] | list[Building]
) -> None:
    """
    Checks the permission of a user for a specific building.

    Parameters:
    - user (User): The user object for which the permission needs to be checked.
    - building (int | Building | list[int] | list[Building]): The building ID, Building object, list of building IDs, or list of Building objects for which the permission needs to be checked.
    """
    if user.is_admin:
        return

    if isinstance(building, int):
        __building_id_permission_checker(user, building)
    elif isinstance(building, Building):
        __building_obj_permission_checker(user, building)
    elif isinstance(building, list):
        __building_list_permission_checker(user, building)


def __building_id_permission_checker(user: User, building_id: int) -> None:
    if user.buildings is None or building_id not in [
        building.id for building in user.buildings
    ]:
        raise ForbiddenBuildingAccess([building_id])


def __building_obj_permission_checker(user: User, building: Building) -> None:
    if user.buildings is None or building not in user.buildings:
        raise ForbiddenBuildingAccess([building.id])  # type: ignore


def __building_list_permission_checker(
    user: User, buildings: list[int] | list[Building]
) -> None:
    building_ids = [
        building.id if isinstance(building, Building) else building
        for building in buildings
    ]
    if user.buildings is None or not set(building_ids).issubset(
        set([building.id for building in user.buildings])
    ):
        raise ForbiddenBuildingAccess(building_ids)  # type: ignore


class ForbiddenBuildingAccess(HTTPException):
    def __init__(self, building_ids: list[int]):
        super().__init__(
            status_code=403,
            detail=f"User do not have access to buildings: {building_ids}",
        )
