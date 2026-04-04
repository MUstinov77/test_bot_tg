from aiogram import Bot
from aiogram.filters import Command
from aiogram.types import Message

from core.config import get_config

config = get_config()

class AdminFilter(Command):

    async def __call__(
            self,
            message: Message,
            bot: Bot
    ):
        result = await super().__call__(message, bot)
        if result and (
            message.from_user.id == config.admin_id or
            message.from_user.id == config.dev_id
        ):
            return True
        return False