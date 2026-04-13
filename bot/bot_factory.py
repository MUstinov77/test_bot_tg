from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.scene import SceneRegistry
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
from aiogram.fsm.strategy import FSMStrategy

from bot.core.config import Settings
from bot.routers import main_router
from bot.scenes.admin import AdminScene
from bot.scenes.test import TestScene
from bot.middleware.is_subscribed import IsSubscribedMiddleware



def get_bot(settings: Settings) -> Bot:
    default_bot_properties = DefaultBotProperties(
        parse_mode=ParseMode.HTML,
        disable_notification=True,
    )
    _bot = Bot(
        token=settings.bot_token,
        default=default_bot_properties,
    )
    return _bot


def build_dispatcher(settings: Settings) -> Dispatcher:
    _dp = Dispatcher(
        storage=MemoryStorage(),
        events_isolation=SimpleEventIsolation(),
        fsm_strategy=FSMStrategy.USER_IN_CHAT
    )
    _dp.include_router(main_router)
    
    if settings.check_subscription:

        main_router.message.middleware(
            IsSubscribedMiddleware(
                settings.admin_chat_id, 
                settings.admin_chat_url
            )
        )

    scene_registry = SceneRegistry(_dp)
    scene_registry.add(TestScene)
    scene_registry.add(AdminScene)
    return _dp


async def bot_factory(settings: Settings):

    bot = get_bot(settings)
    dp = build_dispatcher(settings)

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)
