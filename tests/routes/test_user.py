from fastapi.testclient import TestClient
from sqlmodel import Session

from server.models.database.building_db_model import Building  # noqa
from server.models.database.user_db_model import User  # noqa
from server.models.http.requests.user_request_models import UserRegister
from server.repositories.user_repository import UserRepository


def test_user_create(client: TestClient, user: User, db: Session) -> None:
    """Test user endpoint returns authorized user."""
    my_user = UserRegister(
        email="test@mail.com",
        is_admin=True,
        name="Test",
    )
    UserRepository.create(
        session=db,
        user_in=my_user,
        creator=user,
    )
    resp = client.get("/admin/users")
    assert resp.status_code == 200
    data: list[dict] = resp.json()  # noqa
    found = False
    for user_in_response in data:
        if user_in_response["username"] == "test_user":
            found = True
    assert found
    print(data)
