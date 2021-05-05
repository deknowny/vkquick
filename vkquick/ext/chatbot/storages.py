from __future__ import annotations

import dataclasses
import typing as ty

from vkquick.ext.chatbot.wrappers.message import Message, TruncatedMessage, SentMessage
from vkquick.ext.chatbot.utils import random_id as random_id_
from vkquick.cached_property import cached_property

if ty.TYPE_CHECKING:
    from vkquick.base.event import BaseEvent
    from vkquick.ext.chatbot.application import Bot


@dataclasses.dataclass
class NewEvent:
    event: BaseEvent
    bot: Bot
    metadata: dict = dataclasses.field(default_factory=dict)

    @classmethod
    async def from_event(
        cls, *,
        event: BaseEvent,
        bot: Bot,
    ):
        return cls(event=event, bot=bot)

@dataclasses.dataclass
class NewMessage(NewEvent, SentMessage):

    # _extended_message: Message
    # _sent_message: SentMessage

    @classmethod
    async def from_event(
        cls, *,
        event: BaseEvent,
        bot: Bot,
    ):
        if event.type == 4:
            extended_message = await bot.api.method(
                "messages.get_by_id",
                message_ids=event.content[1],
            )
        elif "message" in event.object:
            extended_message = event.object["message"]
        else:
            extended_message = event.object

        extended_message = Message(extended_message)

        return cls(event=event, bot=bot, api=bot.api, message=extended_message)

    @cached_property
    def msg(self) -> Message:
        return ty.cast(Message, self.message)
