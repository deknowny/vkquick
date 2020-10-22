"""
Управление событиями LongPoll
"""
from __future__ import annotations
import abc
import urllib.parse
import typing as ty

import vkquick.api
import vkquick.current
import vkquick.events_generators.event
import vkquick.utils


class LongPollBase(abc.ABC):
    @abc.abstractmethod
    async def setup(self) -> None:
        """
        Обновляет или достает информацию о LongPoll сервере
        и открывает соединение
        """

    @abc.abstractmethod
    def __aiter__(self) -> LongPollBase:
        """
        Async итерация для получения событий
        """

    @abc.abstractmethod
    def __anext__(self) -> ty.List[vkquick.events_generators.event.Event]:
        ...

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


class GroupLongPoll(LongPollBase):
    """
    LongPoll обработчик для событий в сообществе
    """

    api: vkquick.api.API = vkquick.current.fetch(
        "api_lp_group", "api_lp", "api"
    )

    def __init__(
        self, group_id: ty.Optional[int] = None, wait: int = 25
    ) -> None:
        if (
            group_id is None
            and self.api.token_owner == vkquick.api.TokenOwner.USER
        ):
            raise ValueError(
                "Can't use group longpoll with user token without `group_id`"
            )
        self.group_id = group_id
        self.wait = wait
        self.requests_session = vkquick.utils.RequestsSession("lp.vk.com")
        self.json_parser = vkquick.utils.JSONParserBase.choose_parser()

        self._server_path = self._params = self._lp_settings = None

    def __aiter__(self):
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
        body = await self.requests_session.fetch_body()
        body = self.json_parser.loads(body)
        response = vkquick.events_generators.event.Event(body)

        if "failed" in response:
            await self._resolve_faileds(response)
            return []
        else:
            self._lp_settings.update(ts=response.ts)
            return response.updates

    async def setup(self) -> None:
        new_lp_settings = await self.api.groups.getLongPollServer(
            group_id=self.group_id
        )
        server_url = new_lp_settings().pop("server")
        server = urllib.parse.urlparse(server_url)
        self._server_path = server.path
        self._lp_settings = dict(
            act="a_check", wait=self.wait, **new_lp_settings.mapping_
        )


class UserLongPoll(LongPollBase):
    """
    LongPoll обработчик для событий пользователя
    """

    api: vkquick.api.API = vkquick.current.fetch(
        "api_lp_user", "api_lp", "api"
    )

    def __init__(self, version: int = 10, wait: int = 25, mode: int = 128):
        self.version = version
        self.wait = wait
        self.mode = mode

        self.requests_session = vkquick.utils.RequestsSession("api.vk.me")
        self.json_parser = vkquick.utils.JSONParserBase.choose_parser()
        self._server_path = self._params = self._lp_settings = None

    def __aiter__(self):
        return self

    async def __anext__(self):
        query_string = urllib.parse.urlencode(self._lp_settings)
        query = (
            f"GET {self._server_path}?{query_string} HTTP/1.1\n"
            "Host: api.vk.me\n\n"
        )
        print(query)
        await self.requests_session.write(query.encode("UTF-8"))
        body = await self.requests_session.fetch_body()
        print(body)
        body = self.json_parser.loads(body)
        response = vkquick.events_generators.event.Event(body)

        if "failed" in response:
            await self._resolve_faileds(response)
            return []
        else:
            self._lp_settings.update(ts=response.ts)
            return response.updates

    async def setup(self) -> None:
        new_lp_settings = await self.api.messages.getLongPollServer(
            lp_version=self.version
        )
        server_url = new_lp_settings().pop("server")
        server = urllib.parse.urlparse(server_url)
        self._server_path = server.path
        self._lp_settings = dict(
            act="a_check",
            wait=self.wait,
            mode=self.mode,
            version=self.version,
            **new_lp_settings(),
        )
