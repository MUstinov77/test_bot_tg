from aiogram import Router

from routers import admin_panel, start, test
from core.config import get_config
from core.enum import ProjectStatus
from middleware.is_subscribed import IsSubsribesMiddleware


settings = get_config()

main_router = Router()

main_router.include_router(start.router)
main_router.include_router(test.router)
if settings.project_status == ProjectStatus.premium:
    main_router.include_router(admin_panel.router)