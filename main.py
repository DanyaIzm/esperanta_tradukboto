import asyncio
from scrapper.dictionary import Dictionary
from scrapper.searcher import Searcher
from aiohttp.client import ClientSession


async def main():
    async with ClientSession() as session:
        dick = Dictionary(session)
        resp = await dick.get_html("ĉambro")
        print(resp)


if __name__ == "__main__":
    asyncio.run(main())
