from __future__ import annotations
import datetime
import functools
from vkquick.utils import AttrDict
import typing as ty

from vkquick.base.wrapper import Wrapper


"""
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
"""


class Message(Wrapper):
    @property
    def text(self) -> str:
        return self.fields.text

    @property
    def peer_id(self) -> int:
        return self.fields.peer_id

    @property
    def from_id(self):
        return self.fields.from_id

    @functools.cached_property
    def date(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(
            self.fields.date
        )

    @property
    def conversation_message_id(self) -> int:
        return self.fields.conversation_message_id

    @property
    def id(self) -> int:
        return self.fields.id

    @property
    def out(self) -> bool:
        return bool(self.fields.out)

    @property
    def attachments(self) -> ty.List[AttrDict]:
        return self.fields.conversation_message_id
