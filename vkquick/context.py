from __future__ import annotations
import datetime
import typing as ty

import pydantic

import vkquick.utils
import vkquick.base.debugger
import vkquick.event_handling.handling_info_scheme
import vkquick.wrappers.user


class ClientInfo(pydantic.BaseModel):
    button_actions: ty.List[str]
    keyboard: bool
    inline_keyboard: bool
    carousel: bool
    lang_id: bool


class Message(pydantic.BaseModel):

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
    def from_group_event(cls, event) -> Message:
        ...

    @classmethod
    async def from_user_event(cls, event) -> Message:
        ...

    @classmethod
    async def from_conversation_message(cls, id_: int) -> Message:
        ...

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
    filters_response: ty.Dict[str, vkquick.base.debugger.HandlingStatus] = pydantic.Field(default_factory=dict)
    extra: vkquick.utils.AttrDict = pydantic.Field(default_factory=vkquick.utils.AttrDict)
