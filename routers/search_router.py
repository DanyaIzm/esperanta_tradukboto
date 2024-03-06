from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiohttp import ClientSession
from exceptions import IncorrectArgumentsException
from scrapper import Searcher


router = Router()


@router.message(Command("f"), flags={"throttling_key": "default"})
async def command_f_handler(
    message: Message, command: CommandObject, session: ClientSession
):
    try:
        searcher = Searcher(session)

        if not command.args:
            raise IncorrectArgumentsException("Ne trovis argumentojn")

        args = command.args.split(" ")

        if len(args) != 1:
            raise IncorrectArgumentsException("Ne regula kvanto de argumentoj")

        search_results = await searcher.search(args[0])

        response_text = "\n".join([r.value for r in search_results])

        await message.answer(text=response_text)
    except IncorrectArgumentsException as e:
        error_text = f"{e}!\n\nUzu la /help komandon por ekscii la regulan komanduzadon"

        await message.answer(text=error_text)
