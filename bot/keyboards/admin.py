from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

KEY_ADMIN_MAIL = InlineKeyboardButton(
    text="📩Рассылка",
    callback_data="admin_mail",
)

KEY_ADMIN_BACK = InlineKeyboardButton(
    text="🔙Выйти",
    callback_data="admin_back",
)

KEY_ADMIN_TEST = InlineKeyboardButton(
    text="📝Тесты",
    callback_data="admin_tests",
)

KEY_ADMIN_USERS = InlineKeyboardButton(
    text="👥Пользователи",
    callback_data="admin_users",
)


ADMIN_KEYBOARD = InlineKeyboardBuilder(
    [
        [KEY_ADMIN_MAIL, KEY_ADMIN_USERS],
        [KEY_ADMIN_BACK]
    ]
)