"""
Управление событиями LongPoll
"""
import asyncio
import ssl
import urllib.parse
import typing as ty

import orjson

import vkquick.current
import vkquick.events_generators.event
import vkquick.request


class LongPoll:
    """
    LongPoll обработчик для событий в сообществе
    """

    api = vkquick.current.fetch("api_lp", "api")

    def __init__(self, group_id: int, wait: int = 25):
        self.group_id = group_id
        self.wait = wait
        self.requests_session = vkquick.request.RequestsSession("lp.vk.com")

        self._server_path = (
            self._params
        ) = self.reader = self.writer = self._lp_settings = None

    def __aiter__(self):
        """
        Async итерация для получения событий
        """
        return self

    async def __anext__(
        self,
    ) -> ty.List[vkquick.events_generators.event.Event]:
        query_string = urllib.parse.urlencode(self._lp_settings)
        query = (
            f"GET {self._server_path}?{query_string} HTTP/1.1\n"
            "Host: lp.vk.com\n\n"
        )
        await self.requests_session.write(query.encode("UTF-8"))
        body = await self.requests_session.read_body()
        body = orjson.loads(body)
        response = vkquick.events_generators.event.Event(body)

        if "failed" in response:
            await self._resolve_faileds(response)
            return []
        else:
            self._lp_settings.update(ts=response.ts)
            return response.updates

    async def setup(self):
        """
        Обновляет или достает информацию о LongPoll сервере
        и открыват соединение
        """

        new_lp_settings = await self.api.groups.getLongPollServer(
            group_id=self.group_id
        )
        server_url = new_lp_settings.pop("server")
        server = urllib.parse.urlparse(server_url)
        self._server_path = server.path
        self._lp_settings = dict(
            act="a_check", wait=self.wait, **new_lp_settings
        )

    async def _resolve_faileds(
        self, response: vkquick.events_generators.event.Event
    ):
        """
        Обрабатывает LongPoll ошибки (faileds)
        """
        if response.failed == 1:
            self._lp_settings.update(ts=response.ts)
        elif response.failed in (2, 3):
            await self.setup()
