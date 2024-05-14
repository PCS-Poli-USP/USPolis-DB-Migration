from fastapi import APIRouter, Depends

from server.routes.admin.building_admin_routes import router as AdminBuildingRouter
from server.routes.admin.holiday_category_routes import (
    router as AdminHolidayCategoryRouter,
)
from server.routes.admin.user_admin_routes import router as AdminUserRouter
from server.services.auth.authenticate import admin_authenticate

router = APIRouter(
    prefix="/admin", tags=["Admin"], dependencies=[Depends(admin_authenticate)]
)

router.include_router(AdminUserRouter)
router.include_router(AdminBuildingRouter)
router.include_router(AdminHolidayCategoryRouter)
