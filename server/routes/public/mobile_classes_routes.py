from fastapi import APIRouter

from server.deps.session_dep import SessionDep
from server.models.database.class_db_model import Class
from server.repositories.class_repository import ClassRepository
from server.repositories.classroom_repository import ClassroomRepository
from server.routes.public.dtos.mobile_class_response import MobileClassResponse

router = APIRouter(prefix="/mobile/classes", tags=["Mobile","Classes"])

@router.get("")
async def get_all_classes(session: SessionDep) -> list[MobileClassResponse]:
    """Get all classes, converted to mobile use"""
    classes: list[Class] = ClassRepository.get_all(session=session)
    return MobileClassResponse.from_model_list(classes)