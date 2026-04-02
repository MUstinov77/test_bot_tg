from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_dynamic_keyboard(
        content
):
    builder = ReplyKeyboardBuilder()
    for item in content:
        builder.button(text=str(item).title())
    builder.adjust(2)
    return builder

def get_enumerated_keyboard(num: int):
    builder = ReplyKeyboardBuilder()
    for i in range(1, num + 1):
        builder.button(text=str(i))
    return builder