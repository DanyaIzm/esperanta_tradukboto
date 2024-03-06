import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import ErrorEvent
from aiogram.utils.markdown import hcode
from dotenv import load_dotenv

from routers import register_all_routers


def get_error_handler(admin_id: int):
    async def handler(event: ErrorEvent, bot: Bot):
        await event.update.message.answer(f"Subita eraro okazis!")

        user_id = event.update.message.from_user.id
        username = event.update.message.from_user.username

        username = (
            username
            if username
            else f"{event.update.message.from_user.first_name} {event.update.message.from_user.last_name}"
        )

        to_admin_text = f'Exception from user {username} <a href="tg://user?id={user_id}">{user_id}</a>:\n{hcode(event.exception.__class__)}({event.exception})'

        await bot.send_message(chat_id=admin_id, text=to_admin_text)

        logging.error("Occured an error caused by %s", event.exception, exc_info=True)

    return handler


async def main() -> None:
    load_dotenv()

    dp = Dispatcher()

    register_all_routers(dp)

    dp.error()(get_error_handler(os.getenv("ADMIN_ID")))

    token = os.getenv("BOT_TOKEN")
    bot = Bot(token, parse_mode=ParseMode.HTML)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
