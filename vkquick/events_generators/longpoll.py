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


class LongPoll:
    """
    LongPoll обработчик для событий в сообществе
    """

    api = vkquick.current.fetch("api_lp", "api")

    def __init__(self, group_id: int, wait: int = 25):
        self.group_id = group_id
        self.wait = wait
        self.lock = asyncio.Lock()

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
        self.writer.write(query.encode("utf-8"))
        await self.writer.drain()
        content_length = 0
        async with self.lock:
            while True:
                line = await self.reader.readline()
                if line.startswith(b"Content-Length"):
                    line = line.decode("utf-8")
                    length = ""
                    for i in line:
                        if i.isdigit():
                            length += i
                    content_length = int(length)
                if line == b"\r\n":
                    break

            body = await self.reader.read(content_length)
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

        self.reader, self.writer = await asyncio.open_connection(
            "lp.vk.com", 443, ssl=ssl.SSLContext()
        )

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
