from __future__ import annotations

import dataclasses
import typing as ty

from vkquick.cached_property import cached_property
from vkquick.chatbot.wrappers.message import Message, SentMessage
from vkquick.chatbot.wrappers.page import Group, Page, User

if ty.TYPE_CHECKING:
    from vkquick.base.event import BaseEvent
    from vkquick.chatbot.application import Bot


@dataclasses.dataclass
class NewEvent:
    event: BaseEvent
    bot: Bot
    metadata: dict = dataclasses.field(default_factory=dict)

    @classmethod
    async def from_event(
        cls,
        *,
        event: BaseEvent,
        bot: Bot,
    ):
        return cls(event=event, bot=bot)


SenderTypevar = ty.TypeVar("SenderTypevar", bound=Page)


@dataclasses.dataclass
class NewMessage(NewEvent, SentMessage):
    @classmethod
    async def from_event(
        cls,
        *,
        event: BaseEvent,
        bot: Bot,
    ):
        if event.type == 4:
            extended_message = await bot.api.method(
                "messages.get_by_id",
                message_ids=event.content[1],
            )
            extended_message = extended_message["items"][0]
        elif "message" in event.object:
            extended_message = event.object["message"]
        else:
            extended_message = event.object

        extended_message = Message(extended_message)

        return cls(
            event=event,
            bot=bot,
            api=bot.api,
            truncated_message=extended_message,
        )

    @cached_property
    def msg(self) -> Message:
        return ty.cast(Message, self.truncated_message)

    async def fetch_sender(
        self, typevar: ty.Type[SenderTypevar], /
    ) -> SenderTypevar:
        if self.msg.from_id > 0 and typevar in {Page, User}:
            return await User.fetch_one(self.api, self.msg.from_id)
        elif self.msg.from_id < 0 and typevar in {Page, Group}:
            return await Group.fetch_one(self.api, self.msg.from_id)
        else:
            raise ValueError(
                f"Can't make wrapper with typevar `{typevar}` and from_id `{self.msg.from_id}`"
            )

    def __repr__(self):
        return f"<vkquick.NewMessage text={self.msg.text!r}>"
