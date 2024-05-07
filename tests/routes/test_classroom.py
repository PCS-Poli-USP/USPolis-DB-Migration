import pytest
from httpx import AsyncClient
from fastapi import status

from tests.utils.user_test_utils import get_test_admin_user
from tests.utils.building_test_utils import get_testing_building
from tests.utils.classroom_test_utils import make_classroom_register_input, add_classroom

from tests.utils.enums.test_classroom_enum import ClassroomDefaultValues

from server.models.database.classroom_db_model import Classroom

MAX_CLASSROOM_COUNT = 5


@pytest.mark.asyncio
async def test_classroom_get_all(client: AsyncClient):
    user = await get_test_admin_user()
    building = await get_testing_building()

    for i in range(MAX_CLASSROOM_COUNT):
        await add_classroom(f"{ClassroomDefaultValues.NAME} {i}", building, user)

    response = await client.get("/classrooms")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == MAX_CLASSROOM_COUNT


@pytest.mark.asyncio
async def test_classroom_get(client: AsyncClient):
    user = await get_test_admin_user()
    building = await get_testing_building()

    classroom_id = await add_classroom(ClassroomDefaultValues.NAME, building, user)

    response = await client.get(f"/classrooms/{classroom_id}")
    data = response.json()

    assert data["_id"] == classroom_id
    assert data["name"] == ClassroomDefaultValues.NAME
    assert data["created_by"]["id"] == str(user.id)
    assert data["building"]["id"] == str(building.id)


@pytest.mark.asyncio
async def test_classroom_create(client: AsyncClient):
    user = await get_test_admin_user()
    building = await get_testing_building()

    building_id = str(building.id)
    register = make_classroom_register_input(
        ClassroomDefaultValues.NAME, building_id)
    classroom_input = dict(register)

    response = await client.post("/classrooms", json=classroom_input)
    assert response.status_code == status.HTTP_200_OK

    classroom_id = response.json()
    classroom = await Classroom.get(classroom_id, fetch_links=True)

    user_id = str(user.id)
    assert str(classroom.building.id) == building_id
    assert str(classroom.created_by.id) == user_id
    assert classroom.name == register.name


@pytest.mark.asyncio
async def test_classroom_update(client: AsyncClient):
    user = await get_test_admin_user()
    building = await get_testing_building()
    building_id = str(building.id)
    classroom_id = await add_classroom(ClassroomDefaultValues.NAME, building, user)

    register = make_classroom_register_input(
        f"{ClassroomDefaultValues.NAME} Updated", building_id)
    classroom_input = dict(register)

    response = await client.patch(f"/classrooms/{classroom_id}", json=classroom_input)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == classroom_id

    updated_classroom = await Classroom.by_id(classroom_id)
    assert updated_classroom.name == register.name


@pytest.mark.asyncio
async def test_classroom_delete(client: AsyncClient):
    user = await get_test_admin_user()
    building = await get_testing_building()
    classroom_id = await add_classroom(ClassroomDefaultValues.NAME, building, user)

    response = await client.delete(f"/classrooms/{classroom_id}")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == 1

    building_id = str(building.id)
    assert not await Classroom.check_classroom_name_exists(building_id, ClassroomDefaultValues.NAME)
