from __future__ import annotations
import datetime
import typing as ty

import pydantic

from vkquick.events_generators.event import Event
import vkquick.utils
import vkquick.base.debugger
import vkquick.event_handling.handling_info_scheme
import vkquick.wrappers.user
import vkquick.current


class ClientInfo(pydantic.BaseModel):
    button_actions: ty.List[str]
    keyboard: bool
    inline_keyboard: bool
    carousel: bool
    lang_id: bool


class Message(pydantic.BaseModel):

    # Property игнорируются pydantic
    api = vkquick.current.fetch("api_message", "api")

    class Config:
        extra = "allow"
        allow_mutation = False

    id: int
    date: datetime.datetime
    peer_id: int
    from_id: int
    text: str
    random_id: int
    attachments: ty.List[dict]
    important: bool
    is_hidden: bool
    out: bool
    keyboard: pydantic.Json
    fwd_messages: ty.List[Message]
    geo: ty.Optional[dict]
    payload: ty.Optional[pydantic.Json]
    reply_message: ty.Optional[Message]
    action: ty.Optional[dict]
    ref: ty.Optional[str]
    ref_source: ty.Optional[str]

    @classmethod
    def from_group_event(cls, event: Event) -> Message:
        return cls.parse_obj(event.get_message_object())

    @classmethod
    async def from_user_event(cls, event: Event) -> Message:
        api = cls.api.__get__(cls)
        extended_event = await api.messages.get_by_id(message_ids=event[0])
        extended_event = extended_event[0]
        return cls.parse_obj(extended_event)

    @classmethod
    async def from_conversation_message(
        cls, id_: int, peer_id: int
    ) -> Message:
        # TODO: extendeds
        api = cls.api.__get__(cls)
        extended_event = await api.messages.get_by_conversation_message_id(
            peer_id=peer_id, conversation_message_ids=id_
        )
        extended_event = extended_event[0]
        return cls.parse_obj(extended_event)

    async def answer(self, *args, **kwargs):
        ...

    async def reply(self, *args, **kwargs):
        ...

    async def forward(self, *args, **kwargs):
        ...

    async def fetch_replied_message_sender(self, fields, name_case):
        ...

    async def fetch_forward_messages_sender(self, fields, name_case):
        ...

    async def fetch_attached_user(self):
        ...

    async def fetch_sender(self, fields, name_case):
        ...

    def get_photos(self):
        ...

    def get_docs(self):
        ...


class Context(pydantic.BaseModel):
    message: Message
    client_info: ClientInfo
    filters_response: ty.Dict[
        str, vkquick.base.debugger.HandlingStatus
    ] = pydantic.Field(default_factory=dict)
    extra: vkquick.utils.AttrDict = pydantic.Field(
        default_factory=vkquick.utils.AttrDict
    )
