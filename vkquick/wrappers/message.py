from __future__ import annotations
import datetime
import typing as ty

import pydantic

from vkquick import API
from vkquick.events_generators.event import Event
from vkquick.utils import AttrDict


class MessagesSendResponse:
    """
    Для ответов, содержащих поля peer_ids
    """

    peer_id: int
    message_id: int
    conversation_message_id: int


class Message(pydantic.BaseModel):
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
    async def from_user_event(cls, api: API, event: Event) -> Message:
        extended_event = await api.messages.get_by_id(
            allow_cache_=True, message_ids=event[1]
        )
        extended_event = extended_event.items[0]
        return cls.parse_obj(extended_event())

    @classmethod
    async def from_conversation_message(
        cls, api: API, id_: int, peer_id: int
    ) -> Message:
        # TODO: extendeds
        extended_event = await api.messages.get_by_conversation_message_id(
            allow_cache_=True, peer_id=peer_id, conversation_message_ids=id_
        )
        extended_event = extended_event[0]
        return cls.parse_obj(extended_event)


# Для возможности полей использовать Message
# в своих же полях (ссылки на самого себя)
Message.update_forward_refs()


class ClientInfo(pydantic.BaseModel):
    button_actions: ty.List[str]
    keyboard: bool
    inline_keyboard: bool
    carousel: bool
    lang_id: bool
