from __future__ import annotations

import typing

import aiohttp

from vkquick.api import API, TokenOwner
from vkquick.base.event_factories import BaseLongPoll, EventsCallback
from vkquick.event import GroupEvent, UserEvent

if typing.TYPE_CHECKING:  # pragma: no cover
    from vkquick.base.json_parser import BaseJSONParser


class GroupLongPoll(BaseLongPoll):
    def __init__(
        self,
        api: API,
        /,
        *,
        group_id: typing.Optional[int] = None,
        wait: int = 25,
        new_event_callbacks: typing.Optional[
            typing.List[EventsCallback]
        ] = None,
        requests_session: typing.Optional[aiohttp.ClientSession] = None,
        json_parser: typing.Optional[BaseJSONParser] = None,
    ) -> None:
        super().__init__(
            api=api,
            event_wrapper=GroupEvent,
            new_event_callbacks=new_event_callbacks,
            requests_session=requests_session,
            json_parser=json_parser,
        )
        self._group_id = group_id
        self._wait = wait

    async def _setup(self) -> None:
        await self._define_group_id()
        new_lp_settings = await self.api.groups.get_long_poll_server(
            group_id=self._group_id
        )
        self._server_url = new_lp_settings.pop("server")
        self._requests_query_params = dict(
            act="a_check", wait=self._wait, **new_lp_settings
        )

    async def _define_group_id(self) -> None:
        if self._group_id is None:
            token_owner, owner_schema = await self.api.define_token_owner()
            if token_owner != TokenOwner.GROUP:
                raise ValueError(
                    "Can't use `GroupLongPoll` with user token without `group_id`"
                )
            self._group_id = owner_schema.id


class UserLongPoll(BaseLongPoll):
    def __init__(
        self,
        api: API,
        /,
        *,
        version: int = 3,
        wait: int = 15,
        mode: int = 234,
        new_event_callbacks: typing.Optional[
            typing.List[EventsCallback]
        ] = None,
        requests_session: typing.Optional[aiohttp.ClientSession] = None,
        json_parser: typing.Optional[BaseJSONParser] = None,
    ) -> None:
        super().__init__(
            api=api,
            event_wrapper=UserEvent,
            new_event_callbacks=new_event_callbacks,
            requests_session=requests_session,
            json_parser=json_parser,
        )
        self._version = version
        self._wait = wait
        self._mode = mode

    async def _setup(self) -> None:
        new_lp_settings = await self.api.messages.get_long_poll_server(
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
