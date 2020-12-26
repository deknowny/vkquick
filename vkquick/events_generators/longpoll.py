"""
Управление событиями LongPoll
"""
from __future__ import annotations
import abc
import typing as ty

import aiohttp

from vkquick.json_parsers import json_parser_policy
import vkquick.base.json_parser
import vkquick.json_parsers
import vkquick.events_generators.event
import vkquick.utils


if ty.TYPE_CHECKING:
    from vkquick.api import API


class LongPollBase(abc.ABC):
    """
    Базовый интерфейс для всех типов LongPoll
    """

    _lp_settings: ty.Optional[dict] = None
    session: aiohttp.ClientSession
    server_url: str
    api: API

    def __aiter__(self) -> LongPollBase:
        """
        Итерация запускает процесс получения событий
        """
        return self

    async def __anext__(
        self,
    ) -> ty.List[vkquick.events_generators.event.Event]:
        """
        Отправляет запрос на LongPoll сервер и ждет событие.
        После оборачивает событие в специальную обертку, которая
        в некоторых случаях может сделать интерфейс
        пользовательского лонгпула аналогичным групповому
        """
        async with self.session.get(
            self.server_url, params=self._lp_settings
        ) as response:
            # TODO: X-Next-Ts header
            response = vkquick.utils.AttrDict(
                await response.json(loads=json_parser_policy.loads)
            )

        if "failed" in response:
            await self._resolve_faileds(response)
            return []
        else:
            self._lp_settings.update(ts=response.ts)
            updates = [
                vkquick.events_generators.event.Event(update())
                for update in response.updates
            ]
            return updates

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
        else:
            raise ValueError("Invalid longpoll version")

    async def close_session(self):
        await self.session.close()
        await self.api.close_session()

    @abc.abstractmethod
    async def setup(self) -> None:
        """
        Обновляет или достает информацию о LongPoll сервере
        и открывает соединение
        """

    async def init_session(self):
        self.session = aiohttp.ClientSession(
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
        self.api = api
        if (
            group_id is None
            and self.api.token_owner == vkquick.api.TokenOwner.USER
        ):
            raise ValueError(
                "Can't use group longpoll with user token without `group_id`"
            )
        self.group_id = group_id
        self.wait = wait

        self._server_path = self._params = self._lp_settings = None

    async def setup(self) -> None:
        if self.group_id is None:
            groups = await self.api.groups.get_by_id()
            group = groups[0]
            self.group_id = group.id
        new_lp_settings = await self.api.groups.getLongPollServer(
            group_id=self.group_id
        )
        self.server_url = new_lp_settings().pop("server")
        self._lp_settings = dict(
            act="a_check", wait=self.wait, **new_lp_settings.mapping_
        )
        await self.init_session()


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
        self.api = api
        self.version = version
        self.wait = wait
        self.mode = mode

        self.session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False),
            skip_auto_headers={"User-Agent"},
            raise_for_status=True,
            json_serialize=json_parser_policy.dumps,
        )
        self._server_path = (
            self._params
        ) = self._lp_settings = self._server_netloc = None

    async def setup(self) -> None:
        new_lp_settings = await self.api.messages.getLongPollServer(
            lp_version=self.version
        )
        server_url = new_lp_settings().pop("server")
        self.server_url = f"https://{server_url}"
        self._lp_settings = dict(
            act="a_check",
            wait=self.wait,
            mode=self.mode,
            version=self.version,
            **new_lp_settings(),
        )
        await self.init_session()
