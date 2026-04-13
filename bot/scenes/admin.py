import logging

from aiogram import F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, Message

from bot.core.filters.waiting_mail import WaitingForMail
from bot.keyboards.admin import ADMIN_KEYBOARD
from bot.keyboards.public import CANCEL_KEYBOARD
from bot.keyboards.dynamic import get_dynamic_keyboard
from bot.service.user import get_user_service
from bot.service.test import get_test_service

logger = logging.getLogger()

class AdminScene(Scene, state="admin"):

    @on.message.enter()
    async def on_enter(self, message: Message, state: FSMContext):
        await state.update_data(waiting_mail=False)
        await message.answer(
            "Вы вошли в Админ панель",
            reply_markup=ADMIN_KEYBOARD.as_markup(resize_keyboard=True)
        )

    @on.callback_query(F.data == "admin_users")
    async def admin_users(self, callback: CallbackQuery):
        await callback.answer()
        user_service = await get_user_service()
        users = await user_service.get_all()
        message = f"Всего пользователей: {len(users)}\n"
        for user in users:
            if len(message) > 2048:
                await callback.message.answer(message)
                message = ""
            message += str(user) + "\n"
        await callback.message.answer(message)

    @on.callback_query(F.data == "admin_mail")
    async def admin_mail(self, callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.update_data(waiting_mail=True)
        await callback.message.answer(
            "Введите сообщение для отправки",
            reply_markup=CANCEL_KEYBOARD.as_markup(
                resize_keyboard=True,
                one_time_keyboard=True,
            )
        )

    @on.message(WaitingForMail())
    async def get_message(self, message: Message, state: FSMContext):
        if message.text == "❌ Отмена":
            await state.update_data(waiting_mail=False)
            return await message.answer(
                "Возвращаюсь в меню", 
                reply_markup=ADMIN_KEYBOARD.as_markup(resize_keyboard=True)
            )
        user_service = await get_user_service()
        users = await user_service.get_all()
        for user in users:
            try:
                await message.send_copy(chat_id=user.telegram_id)
            except TelegramBadRequest:
                logger.info(f"chat with user @{user.username} not found")
        await state.update_data(waiting_mail=False)
        await message.answer(
            "Сообщения отправлены",
            reply_markup=ADMIN_KEYBOARD.as_markup(resize_keyboard=True)
        )


    @on.callback_query(F.data == "admin_back")
    async def exit_from_panel(self, callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.update_data(waiting_mail=False)
        await self.wizard.exit()


    @on.callback_query.exit()
    async def on_exit(self, callback: CallbackQuery):
        await callback.answer()
        test_service = await get_test_service()
        tests = await test_service.get_all()
        test_names = [test.name for test in tests]
        await callback.message.answer(
            "Вы вышли из Админ панели",
            reply_markup=get_dynamic_keyboard(test_names).as_markup(resize_keyboard=True)
        )

    @on.message(~WaitingForMail())
    async def unknown_message(self, message: Message):
        await message.answer(
            "Неизвестная команда. Используйте кнопки меню.",
            reply_markup=ADMIN_KEYBOARD.as_markup(resize_keyboard=True)
        )