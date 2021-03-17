"""
Управление событиями LongPoll
"""
from __future__ import annotations

import typing as ty

import aiohttp

from vkquick.bases.events_factories import LongPollBase, EventsCallback
from vkquick.event import GroupEvent, UserEvent
from vkquick.bases.json_parser import JSONParser

if ty.TYPE_CHECKING:  # pragma: no cover
    from vkquick.api import API


class GroupLongPoll(LongPollBase):
    """
    LongPoll обработчик для событий в сообществе
    """

    _event_wrapper = GroupEvent

    def __init__(
        self,
        api: API,
        *,
        group_id: ty.Optional[int] = None,
        wait: int = 25,
        new_event_callbacks: ty.Optional[ty.List[EventsCallback]] = None,
        requests_session: ty.Optional[aiohttp.ClientSession] = None,
        json_parser: ty.Optional[JSONParser] = None,
    ) -> None:
        super().__init__(
            new_event_callbacks=new_event_callbacks,
            requests_session=requests_session,
            json_parser=json_parser,
        )
        self._api = api
        self._group_id = group_id
        self._wait = wait

    async def _setup(self) -> None:
        await self._define_group_id()
        new_lp_settings = await self._api.groups.getLongPollServer(
            group_id=self._group_id
        )
        self._server_url = new_lp_settings.pop("server")
        self._requests_query_params = dict(
            act="a_check", wait=self._wait, **new_lp_settings
        )

    async def _define_group_id(self):
        if self._group_id is None:
            owner = await self._api.fetch_token_owner_entity()
            if not owner.is_group:
                raise ValueError(
                    "Can't use `GroupLongPoll` with user token without `group_id`"
                )
            self._group_id = owner.scheme["id"]


class UserLongPoll(LongPollBase):
    """
    LongPoll обработчик для событий пользователя
    """

    _event_wrapper = UserEvent

    def __init__(
        self,
        api: API,
        *,
        version: int = 3,
        wait: int = 15,
        mode: int = 234,
        new_event_callbacks: ty.Optional[ty.List[EventsCallback]] = None,
        requests_session: ty.Optional[aiohttp.ClientSession] = None,
        json_parser: ty.Optional[JSONParser] = None,
    ):
        super().__init__(
            new_event_callbacks=new_event_callbacks,
            requests_session=requests_session,
            json_parser=json_parser,
        )
        self._api = api
        self._version = version
        self._wait = wait
        self._mode = mode

    async def _setup(self) -> None:
        new_lp_settings = await self._api.messages.getLongPollServer(
            lp_version=self._version
        )
        server_url = new_lp_settings.pop("server")
        self._server_url = f"https://{server_url}"
        self._requests_query_params = dict(
            act="a_check",
            wait=self._wait,
            mode=self._mode,
            version=self._version,
            **new_lp_settings,
        )
