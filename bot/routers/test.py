from aiogram import Router

from core.filters.test_filter import TestFilter
from scenes.test import TestScene

router = Router()

router.message.register(TestScene.as_handler(), TestFilter())
