from typing import Any

from fastapi import APIRouter, Body, Depends

from server.models.user import User
from server.services.auth.cognito import current_user

router = APIRouter(prefix="/test", tags=["Test"])

embed = Body(..., embed=True)


@router.get("")
async def test(user: User = Depends(current_user)) -> Any:
    print(user)
    return {"hello": "world"}
