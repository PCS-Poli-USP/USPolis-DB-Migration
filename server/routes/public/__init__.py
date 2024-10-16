from fastapi import APIRouter
from server.routes.public.forum_routes import router as ForumRouter
from server.routes.public.mobile_classes_routes import router as MobileClassRouter
from server.routes.public.mobile_institutional_events_routes import (
    router as MobileInstitutionalEventsRouter,
)
from server.routes.public.mobile_comments_routes import router as MobileCommentsRouter
from server.routes.public.mobile_google_authentication_routes import (
    router as MobileGAuth,
)
from server.routes.public.mobile_programs_routes import router as ProgramsRouter

router = APIRouter()

router.include_router(ForumRouter)
router.include_router(MobileClassRouter)
router.include_router(MobileInstitutionalEventsRouter)
router.include_router(MobileCommentsRouter)
router.include_router(MobileGAuth)
router.include_router(ProgramsRouter)
