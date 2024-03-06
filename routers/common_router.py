from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from commands import COMMANDS

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    and sends salutation to the user
    """

    response_text = f"Saluton, {hbold(message.from_user.full_name)}!\nVi povas sendi /help komandon por pliscii pri ĉi tia roboto."

    await message.answer(text=response_text)


@router.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    """
    This handler receives messages with `/help` command
    and sends available commands to user with their brief description
    """

    response_text = "Tia roboto havas ĉi tiajn komandojn:\n\n\n"
    response_text += "\n\n".join([f"- {c}: {desc}" for c, desc in COMMANDS.items()])

    await message.answer(text=response_text)
