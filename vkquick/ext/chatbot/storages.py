from __future__ import annotations

import dataclasses
import typing as ty

from vkquick.ext.chatbot.providers.message import MessageProvider, Message

if ty.TYPE_CHECKING:
    from vkquick.base.event import BaseEvent
    from vkquick.ext.chatbot.application import Bot


@dataclasses.dataclass
class NewEvent:
    event: BaseEvent
    bot: Bot
    metadata: dict = dataclasses.field(default_factory=dict)


class NewMessage:
    def __init__(
        self, new_event_storage: NewEvent, mp: MessageProvider
    ):
        self._new_event_storage = new_event_storage
        self._mp = mp

    @classmethod
    async def from_new_event_storage(
        cls, new_event_storage: NewEvent
    ) -> NewMessage:
        # User event
        if new_event_storage.event.type == 4:
            extended_message = await new_event_storage.bot.api.method(
                "messages.get_by_id",
                message_ids=new_event_storage.event.content[1],
            )
        elif "message" in new_event_storage.event.object:
            extended_message = new_event_storage.event.object["message"]
        else:
            extended_message = new_event_storage.event.object

        mp = MessageProvider.from_mapping(
            new_event_storage.bot.api, extended_message
        )
        return cls(new_event_storage, mp)

    @property
    def new_event_storage(self) -> NewEvent:
        return self._new_event_storage

    @property
    def mp(self) -> MessageProvider:
        return self._mp

    @property
    def msg(self) -> Message:
        return self._mp.storage

    @property
    def bot(self) -> Bot:
        return self._new_event_storage.bot
