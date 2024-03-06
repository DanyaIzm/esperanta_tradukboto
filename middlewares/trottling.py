from aiogram.dispatcher.middlewares.base import BaseMiddleware
from cachetools import TTLCache
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Message
from aiogram.dispatcher.flags import get_flag


# https://github.com/MasterGroosha/telegram-casino-bot/blob/aiogram3/bot/middlewares/throttling.py
class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, time: int):
        self.caches = {
            "default": TTLCache(maxsize=10_000, ttl=time),
        }

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        throttling_key = get_flag(data, "throttling_key")
        if throttling_key is not None and throttling_key in self.caches:
            if event.chat.id in self.caches[throttling_key]:
                await event.answer(text="Ĉesu! Ne tiel rapide!")
                return
            else:
                self.caches[throttling_key][event.chat.id] = None
        return await handler(event, data)
