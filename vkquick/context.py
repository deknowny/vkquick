from __future__ import annotations
import typing as ty

import pydantic

from vkquick.events_generators.event import Event
from vkquick.utils import AttrDict
from vkquick.base.handling_status import HandlingStatus
from vkquick.wrappers.message import Message, ClientInfo
from vkquick.wrappers.user import User
from vkquick.current import fetch


class Context(pydantic.BaseModel):

    api = fetch("api_context", "api")

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
        with self.api.synchronize():
            user = self.api.users.get(
                allow_cache_=True, user_ids=self.message.from_id
            )
            user = User(user[0])
        return (
            f"{self.__class__.__name__}"
            f"(from='{user:<fn> <ln>}', "
            f"command='{self.message.text}')"
        )
