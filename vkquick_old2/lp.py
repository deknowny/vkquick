"""
Управление событиями LongPoll
"""
import dataclasses
import ssl
import typing as ty

import aiohttp
import attrdict

from . import current
from .events_handling import event


@dataclasses.dataclass
class LongPoll:
    """
    LongPoll обработчик для событий в сообществе
    """

    group_id: int
    """
    ID Сообщества
    """

    wait: int = 25
    """
    Максимальное время ожидания ответа от сервера
    """

    async def __aenter__(self):
        """
        Вызовите перед итерацией по событиям.

            lp = LongPoll(...)

            async with lp:
                async for events in lp:
                    ...
        """
        self._session = aiohttp.ClientSession()
        await self.get_info()
        return self

    async def __aexit__(self, *_):
        await self.close_session()

    def __aiter__(self):
        """
        Async итерация для получения событий
        """
        self._session = aiohttp.ClientSession()
        return self

    async def __anext__(self) -> ty.List[attrdict.AttrMap]:
        data = dict(act="a_check", wait=self.wait, **self._info)

        async with self._session.post(
            url=self._url, data=data, ssl=ssl.SSLContext()
        ) as response:
            response = await response.json()
            response = event.Event(response)

            if "failed" in response:
                await self._resolve_faileds(response)
                return []
            else:
                self._info.update(ts=response.ts)
                return response.updates

    async def get_info(self):
        """
        Обновляет или достает
        информацию о LongPoll сервере
        """
        info_data = await current.api.groups.getLongPollServer(
            group_id=self.group_id
        )
        self._url = info_data.pop("server")
        self._info = info_data

    async def _resolve_faileds(self, response):
        """
        Обрабатывает LongPoll ошибки (faileds)
        """
        if response.failed == 1:
            self._info.update(ts=response.ts)
        elif response.failed in (2, 3):
            await self.get_info()

    async def close_session(self) -> None:
        await self._session.close()
