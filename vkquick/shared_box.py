import typing

import pydantic

from vkquick.api import API
from vkquick.events_generators.longpoll import LongPollBase

if typing.TYPE_CHECKING:
    from vkquick.bot import Bot


class SharedBox(pydantic.BaseModel):

    class Config:
        extra = "allow"
        arbitrary_types_allowed = True

    api: API
    events_generator: LongPollBase
    bot: "Bot"
