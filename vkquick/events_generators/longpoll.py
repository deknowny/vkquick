"""
Управление событиями LongPoll
"""
from __future__ import annotations

import abc
import asyncio
import typing as ty

import aiohttp

from vkquick.events_generators.event import Event
from vkquick.json_parsers import json_parser_policy

if ty.TYPE_CHECKING:  # pragma: no cover
    from vkquick.api import API


class LongPollBase(abc.ABC):
    """
    Базовый интерфейс для всех типов LongPoll
    """

    def __init__(self):
        self._lp_requests_settings: ty.Optional[ty.Optional[dict]] = None
        self._session: ty.Optional[aiohttp.ClientSession] = None
        self._server_url: ty.Optional[str] = None
        self._api: ty.Optional[API] = None
        self._baked_request = None

    def __aiter__(self) -> LongPollBase:
        """
        Итерация запускает процесс получения событий
        """
        self._setup_called = False
        return self

    async def __anext__(self,) -> ty.List[Event]:
        """
        Отправляет запрос на LongPoll сервер и ждет событие.
        После оборачивает событие в специальную обертку, которая
        в некоторых случаях может сделать интерфейс
        пользовательского лонгпула аналогичным групповому
        """
        if not self._setup_called or self._session.closed:
            await self._setup()
            self._setup_called = True
            self._update_baked_request()

        response = await self._baked_request
        async with response:
            if "X-Next-Ts" in response.headers:
                self._lp_requests_settings.update(
                    ts=response.headers["X-Next-Ts"]
                )
                self._update_baked_request()
                response = await response.json(loads=json_parser_policy.loads)
            else:
                response = await response.json(loads=json_parser_policy.loads)
                await self._resolve_faileds(response)
                self._update_baked_request()
                return []

        updates = [Event(update) for update in response["updates"]]
        return updates

    async def _resolve_faileds(self, response: Event):
        """
        Обрабатывает LongPoll ошибки (faileds)
        """
        if response["failed"] == 1:
            self._lp_requests_settings.update(ts=response["ts"])
        elif response["failed"] in (2, 3):
            await self._setup()
        else:
            raise ValueError("Invalid longpoll version")

    def _update_baked_request(self) -> None:
        self._baked_request = self._session.get(
            self._server_url, params=self._lp_requests_settings
        )
        self._baked_request = asyncio.create_task(self._baked_request)

    async def close_session(self):
        if self._session is not None:
            await self._session.close()
        await self._api.close_session()

    @abc.abstractmethod
    async def _setup(self) -> None:
        """
        Обновляет или достает информацию о LongPoll сервере
        и открывает соединение
        """

    async def _init_session(self):
        self._session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False),
            skip_auto_headers={"User-Agent"},
            raise_for_status=True,
            json_serialize=json_parser_policy.dumps,
        )


class GroupLongPoll(LongPollBase):
    """
    LongPoll обработчик для событий в сообществе

        import asyncio

        import vkquick as vq


        async def main():
            vq.curs.api = vq.API("any-token")
            lp = vq.GroupLongPoll()
            await lp.setup()
            async for events in lp:
                for event in events:
                    print(event)


        asyncio.run(main())

    """

    def __init__(
        self, api: API, *, group_id: ty.Optional[int] = None, wait: int = 25
    ) -> None:
        """
        * `group_id`: Если вы хотите получать события из сообщества через
        пользователя -- этот параметр обязателен. Иначе можно пропустить
        * `wait`: время максимального ожидания от сервера LongPoll
        * `client`: HTTP клиент для отправки запросов
        * `json_parser`: Парсер JSON для новых событий
        """
        super().__init__()
        self._api = api
        if group_id is None and self._api.token_owner == "user":
            raise ValueError(
                "Can't use `GroupLongPoll` with user token without `group_id`"
            )
        self.group_id = group_id
        self.wait = wait

    async def _setup(self) -> None:
        await self._define_group_id()
        new_lp_settings = await self._api.groups.getLongPollServer(
            group_id=self.group_id
        )
        self._server_url = new_lp_settings().pop("server")
        self._lp_requests_settings = dict(
            act="a_check", wait=self.wait, **new_lp_settings()
        )
        await self._init_session()

    async def _define_group_id(self):
        if self.group_id is None:
            groups = await self._api.groups.get_by_id()
            group = groups[0]
            self.group_id = group.id


class UserLongPoll(LongPollBase):
    """
    LongPoll обработчик для событий пользователя


        import asyncio

        import vkquick as vq


        async def main():
            vq.curs.api = vq.API("user-token")
            lp = vq.UserLongPoll()
            await lp.setup()
            async for events in lp:
                for event in events:
                    print(event)


        asyncio.run(main())
    """

    def __init__(
        self, api: API, version: int = 3, wait: int = 15, mode: int = 234
    ):
        """
        * `version`: Версия LongPoll
        * `wait`: Время максимального ожидания от сервера LongPoll
        * `mode`: Битовая макса для указания полей в событии
        * `client`: HTTP клиент для отправки запросов
        * `json_parser`: парсер JSON для новых событий
        """
        super().__init__()
        self._api = api
        self.version = version
        self.wait = wait
        self.mode = mode

    async def _setup(self) -> None:
        new_lp_settings = await self._api.messages.getLongPollServer(
            lp_version=self.version
        )
        server_url = new_lp_settings().pop("server")
        self._server_url = f"https://{server_url}"
        self._lp_requests_settings = dict(
            act="a_check",
            wait=self.wait,
            mode=self.mode,
            version=self.version,
            **new_lp_settings(),
        )
        await self._init_session()
