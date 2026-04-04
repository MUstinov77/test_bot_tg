from aiogram import Router

from core.filters.admin_filter import AdminFilter
from scenes.admin import AdminScene

router = Router()
router.message.register(AdminScene.as_handler(), AdminFilter("admin"))
router.message.filter()