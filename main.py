import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from routers import register_all_routers

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


async def main() -> None:
    dp = Dispatcher()

    register_all_routers(dp)

    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
