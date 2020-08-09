"""
Управление событиями LongPoll
"""
import asyncio
import typing as ty
import ssl
from dataclasses import dataclass

import aiohttp
import attrdict

from . import current


@dataclass
class LongPoll:
    """
    LongPoll обработчик для событий в сообществе
    """

    group_id: int
    """
    ID Сообщества
    """

    info: ty.Optional[attrdict.AttrMap] = None
    """
    Информация о текущем подключении к LongPoll
    """

    wait: int = 25
    """
    Максимальное время ожидания ответа от сервера
    """

    def __aiter__(self):
        """
        Async итерация для получения событий
        """
        self._session = aiohttp.ClientSession()
        return self

    async def __anext__(self) -> attrdict.AttrMap:
        data = dict(act="a_check", wait=self.wait, **self.info)  # required

        # async with self.session:
        async with self._session.post(
            url=self.url, data=data, ssl=ssl.SSLContext()
        ) as response:
            response = await response.json()
            response = attrdict.AttrMap(response)

            self.info.update(ts=response.ts)

            if "failed" in response:
                await self._resolve_faileds(response)
                return []
            else:
                return response.updates

    async def get_info(self):
        """
        Обновляет или достает
        информацию о LongPoll сервере
        """
        info_data = await current.api.groups.getLongPollServer(
            group_id=self.group_id
        )
        self.url = info_data.pop("server")
        self.info = info_data

    async def _resolve_faileds(self, response):
        """
        Обрабатывает LongPoll ошибки (failleds)
        """
        if response.failed == 1:
            self.info.update(ts=response.ts)
        elif response.failed in (2, 3):
            await self.get_info()

    async def close(self) -> None:
        await self._session.close()
