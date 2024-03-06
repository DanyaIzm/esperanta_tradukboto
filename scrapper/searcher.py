from typing import Any
from aiohttp.client import ClientSession
from scrapper.search_result import SearchResult

from scrapper.url import BASE_URL


_SEARCH_URL_POSTFIX = "?ajax=&term="


class Searcher:
    def __init__(self, client: ClientSession) -> None:
        self._session = client

    async def search(self, string: str):
        async with self._session.get(BASE_URL + _SEARCH_URL_POSTFIX + string) as resp:
            json_result = await resp.json(content_type="text/html")

            return self.decode_results(json_result)

    def decode_results(self, data: list[dict[str, Any]]) -> list[SearchResult]:
        return [SearchResult(**e) for e in data]
