from aiogram import Router
from aiogram.types import Message
from aiohttp import ClientSession
from exceptions import AnswerTooLargeException
from scrapper import Dictionary
from aiogram.exceptions import TelegramEntityTooLarge, TelegramBadRequest


router = Router()


@router.message(flags={"throttling_key": "default"})
async def command_f_handler(message: Message, session: ClientSession):
    try:
        dictionary = Dictionary(session)

        if len(message.text) <= 1:
            raise AnswerTooLargeException("Mesaĝo estos tro granda por Telegram")

        cleaned_text = message.text.strip().lower()

        result_html = await dictionary.get_html(cleaned_text)

        if len(result_html) > 4096 * 4:
            raise AnswerTooLargeException("Respondo estos pli ol 4 mesaĝoj")

        # https://github.com/aiogram/aiogram/discussions/963#discussioncomment-3144036
        if len(result_html) > 4096:
            parts = []
            while result_html:
                if len(result_html) <= 4096:
                    parts.append(result_html)
                    break

                part = result_html[:4096]
                first_ln = part.rfind("\n")

                if first_ln != -1:
                    new_part = part[:first_ln]
                    parts.append(new_part)
                    result_html = result_html[first_ln + 1 :]
                else:
                    first_space = part.rfind(" ")

                    if first_space != -1:
                        new_part = part[:first_space]
                        parts.append(new_part)
                        result_html = result_html[first_space + 1 :]
                    else:
                        parts.append(part)
                        result_html = result_html[4096:]

            for part in parts:
                await message.answer(text=part)
        else:
            await message.answer(text=result_html)
    except (TelegramEntityTooLarge, AnswerTooLargeException, TelegramBadRequest):
        error_text = f"Ŝajnas ke la mesaĝo estas tro granda. Bonvolu sendi vorto kun pli da literojn ol kiom vi sendis jam."

        await message.answer(text=error_text)
