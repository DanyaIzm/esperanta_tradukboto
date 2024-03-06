from aiogram import Dispatcher
from .common_router import router as common_router
from .search_router import router as search_router
from .dictionary_router import router as dictionary_router
from middlewares.session_middleware import SessionMiddleware


def register_all_routers(dp: Dispatcher) -> None:
    search_router.message.middleware(SessionMiddleware())
    dictionary_router.message.middleware(SessionMiddleware())

    dp.include_routers(common_router, search_router, dictionary_router)
