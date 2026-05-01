from aiogram import Router

from bot.routers import admin_panel, test
from bot.routers import start
from bot.core.config import settings
from bot.core.enum import ProjectStatus


main_router = Router()

main_router.include_router(start.router)
main_router.include_router(test.router)
if settings.project_status == ProjectStatus.premium:
    main_router.include_router(admin_panel.router)