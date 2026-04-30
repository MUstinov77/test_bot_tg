import logging

from aiogram import F
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.scene import ScenesManager
from aiogram.types import CallbackQuery, Message

from bot.core.config import get_config
from bot.keyboards.dynamic import get_dynamic_keyboard
from bot.models.user import User
from bot.schema.user import UserSchema
from bot.service.test import get_test_service
from bot.service.user import get_user_service


router = Router()
settings = get_config()
logger = logging.getLogger()

@router.message(CommandStart())
async def cmd_start(
        message: Message,
        scenes: ScenesManager
):
    await scenes.close()
    user_service = await get_user_service()
    user = message.from_user
    existing_user = await user_service.get_scalar_by_field(
        User.telegram_id, 
        user.id
    )
    if not existing_user:
        user_data = UserSchema(
        telegram_id=user.id,
        username=user.username
        )
        logger.info(f"user with id {user.id} not found in DB")
        user_service = await get_user_service()
        await user_service.create_instance(user_data.model_dump())
    logger.info("продолжаю работу")
    test_service = await get_test_service()
    tests = await test_service.get_all()
    tests_names = [test.name for test in tests]
    if (
            message.from_user.id == settings.admin_id or
            message.from_user.id == settings.dev_id
    ):
        tests_names.append("Управление")
    await message.answer(
        "Привет, я бот. Я умею проводить тестирование.",
        reply_markup=get_dynamic_keyboard(tests_names).as_markup(
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


@router.callback_query(F.data == "check_subscription")
async def check_subscription(callback: CallbackQuery):
    user = await callback.bot.get_chat_member(
        settings.admin_chat_id,
        callback.from_user.id,
    )

    if user.status in {"member", "administrator", "creator"}:
        await callback.answer("Подписка найдена")
        await callback.message.answer("Отлично, вы подписаны! Теперь используйте /start")
        return

    await callback.answer("Вы еще не подписаны", show_alert=True)
