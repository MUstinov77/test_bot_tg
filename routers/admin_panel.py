from aiogram import Router, F

from core.filters.admin_filter import AdminFilter, CommandAdminFilter
from scenes.admin import AdminScene

router = Router()
router.message.register(AdminScene.as_handler(), CommandAdminFilter("admin"))