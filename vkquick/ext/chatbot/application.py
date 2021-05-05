from __future__ import annotations

import asyncio
import dataclasses
import typing as ty

from vkquick import GroupLongPoll, UserLongPoll
from vkquick.api import API, TokenOwner
from vkquick.base.event_factories import BaseEventFactory
from vkquick.ext.chatbot.package import Package
from vkquick.ext.chatbot.storages import NewEvent, NewMessage


@dataclasses.dataclass
class App(Package):

    packages: ty.List[Package] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.packages.append(self)
        for package in self.packages:
            for command in package.commands:
                command.update_prefix(*self.prefixes)

    async def route_event(self, new_event_storage) -> None:
        routing_coroutines = [
            package.handle_event(new_event_storage)
            for package in self.packages
        ]
        await asyncio.gather(*routing_coroutines)

    async def route_message(self, message_storage: NewMessage):
        routing_coroutines = [
            package.handle_message(message_storage)
            for package in self.packages
        ]
        await asyncio.gather(*routing_coroutines)

    def add_package(self, package: Package) -> None:
        self.packages.append(package)

    def run(self, *tokens: str) -> None:
        asyncio.run(self.coroutine_run(*tokens))

    async def coroutine_run(self, *tokens) -> None:
        bots_init_coroutines = [
            Bot.via_token(token, self) for token in tokens
        ]
        bots = await asyncio.gather(*bots_init_coroutines)
        await self._call_startup(*bots)
        run_coroutines = [bot.run_polling() for bot in bots]
        try:
            await asyncio.gather(*run_coroutines)
        finally:
            await self._call_shutdown(*bots)

    async def _call_startup(self, *bots: Bot) -> None:
        startup_coroutines = []
        for pkg in self.packages:
            for startup_handler in pkg.startup_handlers:
                for bot in bots:
                    startup_coroutines.append(startup_handler(bot))

        await asyncio.gather(*startup_coroutines)

    async def _call_shutdown(self, *bots: Bot) -> None:
        shutdown_coroutines = []
        for pkg in self.packages:
            for shutdown_handler in pkg.shutdown_handlers:
                for bot in bots:
                    shutdown_coroutines.append(shutdown_handler(bot))

        await asyncio.gather(*shutdown_coroutines)


@dataclasses.dataclass
class Bot:
    app: App
    api: API
    events_factory: BaseEventFactory

    @classmethod
    async def via_token(cls, token: str, app: App) -> Bot:
        api = API(token)
        token_owner = await api.define_token_owner()
        events_factory: BaseEventFactory
        if token_owner is TokenOwner.USER:
            events_factory = UserLongPoll(api)
        else:
            events_factory = GroupLongPoll(api)
        return cls(app=app, api=api, events_factory=events_factory)

    async def run_polling(self):
        async for event in self.events_factory.listen():
            new_event_storage = NewEvent(event=event, bot=self)
            asyncio.create_task(self.handle_event(new_event_storage))

    async def handle_event(self, new_event_storage: NewEvent):
        # Запуск обработки события
        asyncio.create_task(self.app.route_event(new_event_storage))

        if new_event_storage.event.type in {
            "message_new",
            "message_reply",
            4,
        }:
            message_storage = await NewMessage.from_event(
                event=new_event_storage.event, bot=new_event_storage.bot
            )

            asyncio.create_task(self.app.route_message(message_storage))
