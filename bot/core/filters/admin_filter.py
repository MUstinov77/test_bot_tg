from aiogram.filters import Filter
from aiogram.types import Message

from bot.core.config import get_config

config = get_config()

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
                    message.from_user.id == config.admin_id or
                    message.from_user.id == config.dev_id
                ):
                    return True
            case _:
                return False
        return False
