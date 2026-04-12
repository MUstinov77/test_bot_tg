from aiogram import Router, F

from core.filters.admin_filter import AdminFilter
from scenes.admin import AdminScene

router = Router()
router.message.register(AdminScene.as_handler(), AdminFilter("Управление"))