import typing as ty

import aiohttp

from vkquick.utils import create_aiohttp_session


class AiohttpSessionContainer:

    def __init__(self, requests_session: ty.Optional[aiohttp.ClientSession] = None):
        self.__session = requests_session or None

    @property
    def requests_session(self):
        if self.__session is None:
            self.__session = create_aiohttp_session()

        return self.__session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_session()

    async def close_session(self):
        await self.__session.close()
