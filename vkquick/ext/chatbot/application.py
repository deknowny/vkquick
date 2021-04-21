from __future__ import annotations

import asyncio
import dataclasses

from vkquick.api import API
from vkquick.base.event_factories import BaseEventFactory
from vkquick.ext.chatbot.package import Package
from vkquick.ext.chatbot.storages import NewEventStorage, MessageStorage


class App(Package):
    def run(self, *tokens):
        asyncio.run(self.coroutine_run(*tokens))

    async def coroutine_run(self, *tokens):
        ...


@dataclasses.dataclass
class Bot:
    app: App
    api: API
    events_factory: BaseEventFactory

    async def via_token(self, token, **kwargs):
        ...

    async def run_polling(self):
        async for event in self.events_factory.listen():
            new_event_storage = NewEventStorage(event=event, bot=self)
            asyncio.create_task(self.app.route_event(new_event_storage))
            asyncio.create_task(self.pass_to_commands(new_event_storage))

    async def pass_to_commands(self, new_event_storage: NewEventStorage):
        if new_event_storage.event.type in {
            "message_new",
            "message_reply",
            4,
        }:
            message_storage = await MessageStorage.from_new_event_storage(
                new_event_storage
            )
            await self.app.route_message(message_storage)
