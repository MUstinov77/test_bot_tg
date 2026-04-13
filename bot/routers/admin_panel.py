from aiogram import Router

from bot.core.filters.admin_filter import AdminFilter
from bot.scenes.admin import AdminScene

router = Router()
router.message.register(AdminScene.as_handler(), AdminFilter("Управление"))