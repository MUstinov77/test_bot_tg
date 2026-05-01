from aiogram.filters import Filter
from aiogram.types import Message

from bot.core.config import settings


class AdminFilter(Filter):

    def __init__(self, text: str):
        self.text = text

    async def __call__(
            self,
            message: Message,
    ):
        match message.text:
            case self.text:
                if (
                    message.from_user.id == settings.admin_id or
                    message.from_user.id == settings.dev_id
                ):
                    return True
            case _:
                return False
        return False
