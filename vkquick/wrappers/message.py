from __future__ import annotations
import asyncio
import datetime
import typing as ty

import pydantic

from vkquick.wrappers.user import User
from vkquick.current import fetch
from vkquick.events_generators.event import Event
from vkquick.utils import AttrDict
import vkquick.utils


class MessagesSendResponse:
    """
    Для ответов, содержащих поля peer_ids
    """
    peer_id: int
    message_id: int
    conversation_message_id: int


class Message(pydantic.BaseModel):

    # Property игнорируются pydantic
    api = fetch("api_message", "api")

    class Config:
        extra = "allow"
        allow_mutation = False
        arbitrary_types_allowed = True

    id: int
    date: datetime.datetime
    peer_id: int
    from_id: int
    text: str
    random_id: int
    attachments: ty.List[AttrDict]
    important: bool
    is_hidden: bool
    out: bool
    conversation_message_id: int
    keyboard: pydantic.Json
    fwd_messages: list
    geo: ty.Optional[AttrDict]
    payload: ty.Optional[pydantic.Json]
    reply_message: ty.Optional[AttrDict]
    action: ty.Optional[AttrDict]
    ref: ty.Optional[str]
    ref_source: ty.Optional[str]
    expire_ttl: ty.Optional[int]

    @pydantic.validator("attachments", pre=True)
    def attachments_to_attrdict(cls, value):
        return [AttrDict(i) for i in value]

    @pydantic.validator("geo", pre=True)
    def geo_to_attrdict(cls, value):
        return AttrDict(value)

    @pydantic.validator("reply_message", pre=True)
    def reply_message_to_attrdict(cls, value):
        return AttrDict(value)

    @pydantic.validator("action", pre=True)
    def action_message_to_attrdict(cls, value):
        return AttrDict(value)

    @classmethod
    def from_group_event(cls, event: Event) -> Message:
        return cls.parse_obj(event.object.message())

    @classmethod
    async def from_user_event(cls, event: Event) -> Message:
        api = cls.api.__get__(cls)
        extended_event = await api.messages.get_by_id(
            allow_cache_=True, message_ids=event[1]
        )
        extended_event = extended_event.items[0]
        return cls.parse_obj(extended_event())

    @classmethod
    async def from_conversation_message(
        cls, id_: int, peer_id: int
    ) -> Message:
        # TODO: extendeds
        api = cls.api.__get__(cls)
        extended_event = await api.messages.get_by_conversation_message_id(
            allow_cache_=True, peer_id=peer_id, conversation_message_ids=id_
        )
        extended_event = extended_event[0]
        return cls.parse_obj(extended_event)

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
        params = {"peer_ids": self.peer_id}
        for name, value in locals().items():
            if name == "kwargs":
                params.update(value)
            elif name != "self" and value is not None:
                params.update({name: value})

        del params["params"]

        if random_id is None:
            params["random_id"] = vkquick.utils.random_id()

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
            "peer_ids": self.peer_id,
            f"forward": "{"
            '"is_reply":true,'
            f'"conversation_message_ids":[{self.conversation_message_id}],'
            f'"peer_id":{self.peer_id}'
            "}",
        }
        for name, value in locals().items():
            if name == "kwargs":
                params.update(value)
            elif name != "self" and value is not None:
                params.update({name: value})

        del params["params"]

        if random_id is None:
            params["random_id"] = vkquick.utils.random_id()

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
            "peer_ids": self.peer_id,
            f"forward": "{"
            f'"conversation_message_ids":[{self.conversation_message_id}],'
            f'"peer_id":{self.peer_id}'
            "}",
        }
        for name, value in locals().items():
            if name == "kwargs":
                params.update(value)
            elif name != "self" and value is not None:
                params.update({name: value})

        del params["params"]

        if random_id is None:
            params["random_id"] = vkquick.utils.random_id()

        response = await self.api.method("messages.send", params)
        return response[0]

    async def fetch_replied_message_sender(
        self, fields: ty.Optional[ty.List[str]] = None, name_case: ty.Optional[str] = None
    ) -> ty.Optional[User]:
        if self.reply_message is None:
            return None

        user_id = self.reply_message.from_id
        user = await User.build_from_id(
            user_id, fields=fields, name_case=name_case
        )
        return user

    async def fetch_forward_messages_sender(
        self, fields: ty.Optional[ty.List[str]] = None, name_case: ty.Optional[str] = None
    ) -> ty.List[User]:
        user_tasks = []
        for message in self.fwd_messages:
            user_task = User.build_from_id(
                message.from_id, fields=fields, name_case=name_case
            )
            user_tasks.append(user_task)
        users = await asyncio.gather(*user_tasks)
        return users

    async def fetch_attached_user(
        self, fields: ty.Optional[ty.List[str]] = None, name_case: ty.Optional[str] = None
    ) -> ty.Optional[User]:
        replied_user = await self.fetch_replied_message_sender(
            fields=fields, name_case=name_case
        )
        if replied_user is not None:
            return replied_user
        if not self.fwd_messages:
            return None
        first_user_from_fwd = await User.build_from_id(
            self.fwd_messages[0].from_id, fields=fields, name_case=name_case
        )
        return first_user_from_fwd

    async def fetch_sender(
        self, fields: ty.Optional[ty.List[str]] = None, name_case: ty.Optional[str] = None
    ) -> User:
        sender = await User.build_from_id(
            self.from_id, fields=fields, name_case=name_case
        )
        return sender

    def get_photos(self):
        ...

    def get_docs(self):
        ...


# Для возможности полей использовать Message в своих же полях
Message.update_forward_refs()


class ClientInfo(pydantic.BaseModel):
    button_actions: ty.List[str]
    keyboard: bool
    inline_keyboard: bool
    carousel: bool
    lang_id: bool
