from aiogram import Router

from bot.core.filters.test_filter import TestFilter
from bot.scenes.test import TestScene

router = Router()

router.message.register(TestScene.as_handler(), TestFilter())
