from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

CANCEL_BUTTON = KeyboardButton(text="❌ Отмена")

CANCEL_KEYBOARD = ReplyKeyboardBuilder(
    [[CANCEL_BUTTON]]
)
