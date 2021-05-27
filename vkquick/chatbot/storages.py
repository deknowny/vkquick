from __future__ import annotations

import dataclasses
import functools
import typing

from vkquick.chatbot.utils import peer
from vkquick.chatbot.wrappers.message import (
    CallbackButtonPressedMessage,
    Message,
    SentMessage,
)
from vkquick.chatbot.wrappers.page import Group, Page, User

if typing.TYPE_CHECKING:  # pragma: no cover
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


SenderTypevar = typing.TypeVar("SenderTypevar", bound=Page)


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

    @functools.cached_property
    def msg(self) -> Message:
        return typing.cast(Message, self.truncated_message)

    async def fetch_sender(
        self, typevar: typing.Type[SenderTypevar], /
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


class CallbackButtonPressed(NewEvent):
    @functools.cached_property
    def msg(self) -> CallbackButtonPressedMessage:
        return CallbackButtonPressedMessage(self.event.object)

    async def _call_action(self, **event_data):
        return await self.bot.api.method(
            "messages.send_message_event_answer",
            event_id=self.msg.event_id,
            user_id=self.msg.user_id,
            peer_id=self.msg.peer_id,
            event_data=event_data,
        )

    async def show_snackbar(self, text: str) -> dict:
        return await self._call_action(text=text, type="show_snackbar")

    async def open_link(self, link: str) -> dict:
        return await self._call_action(link=link, type="open_link")

    async def open_app(
        self, app_id: int, hash: str, owner_id: typing.Optional[int] = None
    ) -> dict:
        return await self._call_action(
            app_id=app_id, hash=hash, owner_id=owner_id, type="open_app"
        )
