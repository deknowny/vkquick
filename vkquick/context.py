from __future__ import annotations
import typing as ty

import pydantic

from vkquick.events_generators.event import Event
from vkquick.utils import AttrDict
from vkquick.base.handling_status import HandlingStatus
from vkquick.message import Message, ClientInfo


class Context(pydantic.BaseModel):

    class Config:
        arbitrary_types_allowed = True

    source_event: Event
    message: Message
    client_info: ty.Optional[ClientInfo]
    filters_response: ty.Dict[str, HandlingStatus] = pydantic.Field(
        default_factory=dict
    )
    extra: AttrDict = pydantic.Field(default_factory=AttrDict)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}" \
               f"(source_event, message, client_info, " \
               f"filters_response, extra)"
