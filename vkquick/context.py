from __future__ import annotations
import asyncio
import dataclasses
import typing as ty

import pydantic

from vkquick.wrappers.user import User
from vkquick.events_generators.event import Event
from vkquick.utils import AttrDict, random_id as random_id_
from vkquick.base.handling_status import HandlingStatus
from vkquick.wrappers.message import Message, ClientInfo, MessagesSendResponse
from vkquick.shared_box import SharedBox
from vkquick.api import API


@dataclasses.dataclass
class Context:

    shared_box: SharedBox
    source_event: Event
    message: Message
    client_info: ty.Optional[ClientInfo] = None
    filters_response: ty.Dict[str, HandlingStatus] = dataclasses.field(
        default_factory=dict
    )
    extra: AttrDict = dataclasses.field(default_factory=AttrDict)

    @property
    def api(self) -> API:
        return self.shared_box.api

    async def answer(
        self,
        message: ty.Optional[str] = None,
        /,
        *,
        random_id: ty.Optional[int] = None,
        lat: ty.Optional[float] = None,
        long: ty.Optional[float] = None,
        attachment: ty.Optional[ty.List[str]] = None,
        reply_to: ty.Optional[int] = None,
        forward_messages: ty.Optional[ty.List[int]] = None,
        sticker_id: ty.Optional[int] = None,
        group_id: ty.Optional[int] = None,
        keyboard: ty.Optional[str] = None,
        payload: ty.Optional[str] = None,
        dont_parse_links: ty.Optional[bool] = None,
        disable_mentions: ty.Optional[bool] = None,
        intent: ty.Optional[str] = None,
        expire_ttl: ty.Optional[int] = None,
        silent: ty.Optional[bool] = None,
        subscribe_id: ty.Optional[int] = None,
        content_source: ty.Optional[str] = None,
        forward: ty.Optional[str] = None,
        **kwargs,
    ):
        params = {"peer_ids": self.message.peer_id}
        for name, value in locals().items():
            if name == "kwargs":
                params.update(value)
            elif name != "self" and value is not None:
                params.update({name: value})

        del params["params"]

        if random_id is None:
            params["random_id"] = random_id_()

        return await self.api.method("messages.send", params)

    async def reply(
        self,
        message: ty.Optional[str] = None,
        /,
        *,
        random_id: ty.Optional[int] = None,
        lat: ty.Optional[float] = None,
        long: ty.Optional[float] = None,
        attachment: ty.Optional[ty.List[str]] = None,
        sticker_id: ty.Optional[int] = None,
        group_id: ty.Optional[int] = None,
        keyboard: ty.Optional[str] = None,
        payload: ty.Optional[str] = None,
        dont_parse_links: ty.Optional[bool] = None,
        disable_mentions: ty.Optional[bool] = None,
        intent: ty.Optional[str] = None,
        expire_ttl: ty.Optional[int] = None,
        silent: ty.Optional[bool] = None,
        subscribe_id: ty.Optional[int] = None,
        content_source: ty.Optional[str] = None,
        **kwargs,
    ) -> MessagesSendResponse:
        params = {
            "peer_ids": self.message.peer_id,
            f"forward": "{"
            '"is_reply":true,'
            f'"conversation_message_ids":[{self.message.conversation_message_id}],'
            f'"peer_id":{self.message.peer_id}'
            "}",
        }
        for name, value in locals().items():
            if name == "kwargs":
                params.update(value)
            elif name != "self" and value is not None:
                params.update({name: value})

        del params["params"]

        if random_id is None:
            params["random_id"] = random_id_()

        response = await self.api.method("messages.send", params)
        return response[0]

    async def forward(
        self,
        message: ty.Optional[str] = None,
        /,
        *,
        random_id: ty.Optional[int] = None,
        lat: ty.Optional[float] = None,
        long: ty.Optional[float] = None,
        attachment: ty.Optional[ty.List[str]] = None,
        sticker_id: ty.Optional[int] = None,
        group_id: ty.Optional[int] = None,
        keyboard: ty.Optional[str] = None,
        payload: ty.Optional[str] = None,
        dont_parse_links: ty.Optional[bool] = None,
        disable_mentions: ty.Optional[bool] = None,
        intent: ty.Optional[str] = None,
        expire_ttl: ty.Optional[int] = None,
        silent: ty.Optional[bool] = None,
        subscribe_id: ty.Optional[int] = None,
        content_source: ty.Optional[str] = None,
        **kwargs,
    ) -> MessagesSendResponse:
        params = {
            "peer_ids": self.message.peer_id,
            f"forward": "{"
            f'"conversation_message_ids":[{self.message.conversation_message_id}],'
            f'"peer_id":{self.message.peer_id}'
            "}",
        }
        for name, value in locals().items():
            if name == "kwargs":
                params.update(value)
            elif name != "self" and value is not None:
                params.update({name: value})

        del params["params"]

        if random_id is None:
            params["random_id"] = random_id_()

        response = await self.api.method("messages.send", params)
        return response[0]

    async def fetch_replied_message_sender(
        self,
        fields: ty.Optional[ty.List[str]] = None,
        name_case: ty.Optional[str] = None,
    ) -> ty.Optional[User]:
        if self.message.reply_message is None:
            return None

        user_id = self.message.reply_message.from_id
        user = await User.build_from_id(
            user_id, fields=fields, name_case=name_case
        )
        return user

    async def fetch_forward_messages_sender(
        self,
        fields: ty.Optional[ty.List[str]] = None,
        name_case: ty.Optional[str] = None,
    ) -> ty.List[User]:
        user_tasks = []
        for message in self.message.fwd_messages:
            user_task = User.build_from_id(
                message.from_id, fields=fields, name_case=name_case
            )
            user_tasks.append(user_task)
        users = await asyncio.gather(*user_tasks)
        return users

    async def fetch_attached_user(
        self,
        fields: ty.Optional[ty.List[str]] = None,
        name_case: ty.Optional[str] = None,
    ) -> ty.Optional[User]:
        replied_user = await self.fetch_replied_message_sender(
            fields=fields, name_case=name_case
        )
        if replied_user is not None:
            return replied_user
        if not self.message.fwd_messages:
            return None
        first_user_from_fwd = await User.build_from_id(
            self.message.fwd_messages[0].from_id,
            fields=fields,
            name_case=name_case,
        )
        return first_user_from_fwd

    async def fetch_sender(
        self,
        fields: ty.Optional[ty.List[str]] = None,
        name_case: ty.Optional[str] = None,
    ) -> User:
        sender = await User.build_from_id(
            self.message.from_id, fields=fields, name_case=name_case
        )
        return sender

    def get_photos(self):
        ...

    def get_docs(self):
        ...

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(source_event, message, client_info, "
            f"filters_response, extra)"
        )
