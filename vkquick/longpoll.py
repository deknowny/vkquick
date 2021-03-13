"""
Управление событиями LongPoll
"""
from __future__ import annotations

import typing as ty

from vkquick.bases.events_factories import LongPollBase
from vkquick.bases.event import Event

if ty.TYPE_CHECKING:  # pragma: no cover
    from vkquick.api import API


Callback = ty.Coroutine[[Event], None, None]


class GroupLongPoll(LongPollBase):
    """
    LongPoll обработчик для событий в сообществе
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
