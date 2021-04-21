from __future__ import annotations

import dataclasses

from vkquick import MessageProvider, Message
from vkquick.base import BaseEvent
from vkquick.ext.chatbot.application import Bot


@dataclasses.dataclass
class NewEventStorage:
    event: BaseEvent
    bot: Bot
    metadata: dict = dataclasses.field(default_factory=dict)


class MessageStorage:
    def __init__(
        self, new_event_storage: NewEventStorage, mp: MessageProvider
    ):
        self._new_event_storage = new_event_storage
        self._mp = mp

    @classmethod
    async def from_new_event_storage(
        cls, new_event_storage: NewEventStorage
    ) -> MessageStorage:
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

        mp = MessageProvider.from_wrapper(
            new_event_storage.bot.api, extended_message
        )
        return cls(new_event_storage, mp)

    @property
    def new_event_storage(self) -> NewEventStorage:
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
