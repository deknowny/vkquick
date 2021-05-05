from __future__ import annotations

import dataclasses
import typing as ty

from vkquick import API
from vkquick.cached_property import cached_property
from vkquick.ext.chatbot.utils import random_id as random_id_
from vkquick.ext.chatbot.wrappers import User, Group, Page
from vkquick.ext.chatbot.wrappers.message import (
    Message,
    SentMessage,
    TruncatedMessage,
)

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
        cls,
        *,
        event: BaseEvent,
        bot: Bot,
    ):
        return cls(event=event, bot=bot)

    @property
    def api(self) -> API:
        return self.bot.api


@dataclasses.dataclass
class NewMessage(NewEvent, SentMessage):

    # _extended_message: Message
    # _sent_message: SentMessage

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
        elif "message" in event.object:
            extended_message = event.object["message"]
        else:
            extended_message = event.object

        extended_message = Message(extended_message)

        return cls(
            event=event, bot=bot, api=bot.api, message=extended_message
        )

    @cached_property
    def msg(self) -> Message:
        return ty.cast(Message, self.message)

    async def fetch_any_sender(self) -> Page:
        if self.msg.from_id > 0:
            return await User.fetch_one(
                self.api, self.msg.from_id
            )
        else:
            return await Group.fetch_one(
                self.api, self.msg.from_id
            )

    async def fetch_user_sender(self) -> User:
        if self.msg.from_id < 0:
            raise ValueError(
                "Message was sent by a group. Can't fetch user provider"
            )
        else:
            return await User.fetch_one(
                self.api, self.msg.from_id
            )

    async def fetch_group_sender(self) -> Group:
        if self.msg.from_id > 0:
            raise ValueError(
                "Message was sent by a user. Can't fetch group provider"
            )
        else:
            return await Group.fetch_one(
                self.api, self.msg.from_id
            )
