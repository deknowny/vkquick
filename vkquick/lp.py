"""
Управление событиями LongPoll
"""
import ssl
from dataclasses import dataclass

import aiohttp
import attrdict

from . import current


@dataclass
class LongPoll:
    """
    LongPoll handler for groups
    """

    group_id: int
    wait: int = 25

    def __aiter__(self):
        """
        Async itearation for
        LongPoll listening
        """
        return self

    async def __anext__(self) -> attrdict.AttrMap:
        await self._get_info()
        data = dict(act="a_check", wait=self.wait, **self.info)
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=self.info.server, data=data, ssl=ssl.SSLContext()
            ) as response:
                response = await response.json()
                response = attrdict.AttrMap(response)

                if "failed" in response:
                    await self._resolve_faileds(response)
                else:
                    return response.updates

    async def _get_info(self):
        """
        Set or update LongPoll info
        (key, server, ts)
        """
        self.info = await current.api.groups.getLongPollServer(
            group_id=self.group_id
        )

    async def _resolve_faileds(self, response):
        if response.failed == 1:
            self.info.update(ts=response.ts)
        elif response.failed in (2, 3):
            await self._get_info()
