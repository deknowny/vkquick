"""
Управление событиями LongPoll
"""
from __future__ import annotations
import abc
import typing as ty

import vkquick.api
import vkquick.base.json_parser
import vkquick.base.client
import vkquick.json_parsers
import vkquick.current
import vkquick.events_generators.event
import vkquick.utils
import vkquick.clients


class LongPollBase(abc.ABC):
    _lp_settings: ty.Optional[dict] = None
    session: ty.Optional[vkquick.clients.AIOHTTPClient] = None

    def __aiter__(self):
        return self

    async def __anext__(
        self,
    ) -> ty.List[vkquick.events_generators.event.Event]:
        response = await self.session.send_get_request("", self._lp_settings)
        response = vkquick.utils.AttrDict(response)

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

    @abc.abstractmethod
    async def setup(self) -> None:
        """
        Обновляет или достает информацию о LongPoll сервере
        и открывает соединение
        """


class GroupLongPoll(LongPollBase):
    """
    LongPoll обработчик для событий в сообществе
    """

    api: vkquick.api.API = vkquick.current.fetch(
        "api_lp_group", "api_lp", "api"
    )

    def __init__(
        self,
        group_id: ty.Optional[int] = None,
        wait: int = 25,
        client: ty.Optional[
            ty.Type[vkquick.base.client.AsyncHTTPClient]
        ] = None,
        json_parser: ty.Optional[
            ty.Type[vkquick.base.json_parser.JSONParser]
        ] = None,
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
        self.session = None
        self.client = client or vkquick.clients.AIOHTTPClient
        self.json_parser = (
            json_parser or vkquick.json_parsers.BuiltinJSONParser
        )
        self._server_path = self._params = self._lp_settings = None

    async def setup(self) -> None:
        if self.group_id is None:
            groups = await self.api.groups.get()
            group = groups[0]
            group_id = group.id
        else:
            group_id = self.group_id
        new_lp_settings = await self.api.groups.getLongPollServer(
            group_id=group_id
        )
        server_url = new_lp_settings().pop("server")
        self._lp_settings = dict(
            act="a_check", wait=self.wait, **new_lp_settings.mapping_
        )
        self.session = self.client(server_url, self.json_parser)


class UserLongPoll(LongPollBase):
    """
    LongPoll обработчик для событий пользователя
    """

    api: vkquick.api.API = vkquick.current.fetch(
        "api_lp_user", "api_lp", "api"
    )

    def __init__(
        self,
        version: int = 3,
        wait: int = 15,
        mode: int = 234,
        client: ty.Optional[
            ty.Type[vkquick.base.client.AsyncHTTPClient]
        ] = None,
        json_parser: ty.Optional[
            ty.Type[vkquick.base.json_parser.JSONParser]
        ] = None,
    ):
        self.version = version
        self.wait = wait
        self.mode = mode

        self.client = client or vkquick.clients.AIOHTTPClient
        self.json_parser = (
            json_parser or vkquick.json_parsers.BuiltinJSONParser
        )
        self._server_path = (
            self._params
        ) = self._lp_settings = self._server_netloc = None

    async def setup(self) -> None:
        new_lp_settings = await self.api.messages.getLongPollServer(
            lp_version=self.version
        )
        server_url = new_lp_settings().pop("server")
        self._lp_settings = dict(
            act="a_check",
            wait=self.wait,
            mode=self.mode,
            version=self.version,
            **new_lp_settings(),
        )
        self.session = self.client(f"https://{server_url}", self.json_parser)
