import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest

logger = logging.getLogger(__name__)



class IsSubscribedMiddleware(BaseMiddleware):

    def __init__(
        self, 
        admin_chat_id: int, 
        admin_chat_url: str
    ) -> None:
        self.admin_chat_id = admin_chat_id
        self.admin_chat_url = admin_chat_url
        

    async def __call__(
        self, 
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]], 
        event: Message, 
        data: dict[str, Any],
    ) -> Any:
        bot = data.get("bot")
        try:
            user = await bot.get_chat_member(
                self.admin_chat_id,
                event.from_user.id
            )
        except (TelegramForbiddenError, TelegramBadRequest) as e:
            logger.exception("Bot should have adminstrator rigths or chat does not exists")
            raise
        match user.status:
            case "left" | "kicked":
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="Перейти в канал", url=self.admin_chat_url)],
                        [InlineKeyboardButton(text="Проверить подписку", callback_data="check_subscription")]
                    ]
                )
                await event.answer(
                    "Чтобы продолжить, подпишитесь на канал:",
                    reply_markup=keyboard,
                )
                return None
            case _:
                return await handler(event, data)