from aiohttp import ClientSession
from bs4 import BeautifulSoup

from scrapper.url import BASE_URL


class WordNotFoundException(Exception): ...


class Dictionary:
    def __init__(self, session: ClientSession):
        self._session = session

    async def get_html(self, word: str) -> str:
        html = await self._get_html(word)

        return html

    async def _get_html(self, word: str) -> str:
        word = "+".join(word.split(" "))

        async with self._session.get(BASE_URL + word) as resp:
            resp_text = await resp.text()

        bs = BeautifulSoup(resp_text)
        search_result = bs.find("div", {"class": "search_result"})

        if not search_result:
            raise WordNotFoundException("Ne estas rezulto")

        tag = search_result.find("div")

        divs = tag.find_all("div")

        for div in divs:
            div.replace_with("")

        spans = tag.find_all("span")

        for span in spans:
            span.replace_with(span.text)

        result = (
            str("".join(str(t) for t in tag.contents))
            .replace("<br>", "\n")
            .replace("<br/>", "")
            .replace("</br>", "")
        )

        return result
