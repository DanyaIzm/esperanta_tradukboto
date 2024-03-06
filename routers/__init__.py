from aiogram import Dispatcher
from .common_router import router as common_router


def register_all_routers(dp: Dispatcher) -> None:
    dp.include_routers(common_router)
