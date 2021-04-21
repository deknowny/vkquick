from __future__ import annotations

import asyncio
import dataclasses
import collections
import re
import typing as ty

from vkquick.base.event import EventType

from vkquick.ext.chatbot.base.filter import Filter
from vkquick.ext.chatbot.command.command import Command

if ty.TYPE_CHECKING:
    from vkquick.ext.chatbot.base.middleware import EventMiddleware, MessageMiddleware
    from vkquick.types import DecoratorFunction
    from vkquick.ext.chatbot.application import Bot
    from vkquick.ext.chatbot.storages import NewEventStorage, MessageStorage

SignalHandler = ty.Callable[[Bot], ty.Awaitable]
SignalHandlerTypevar = ty.TypeVar("SignalHandlerTypevar", bound=SignalHandler)


@dataclasses.dataclass
class Package:

    packages: ty.List[Package] = dataclasses.field(default_factory=list)
    event_middlewares: ty.List[EventMiddleware] = dataclasses.field(
        default_factory=list
    )
    message_middlewares: ty.List[MessageMiddleware] = dataclasses.field(
        default_factory=list
    )
    commands: ty.List[Command] = dataclasses.field(default_factory=list)
    event_handlers: ty.Dict[
        EventType, ty.List[ty.Callable[[NewEventStorage], ty.Awaitable]]
    ] = dataclasses.field(
        default_factory=lambda: collections.defaultdict(list)
    )
    startup_handler: ty.Optional[SignalHandler] = None
    shutdown_handler: ty.Optional[SignalHandler] = None

    def command(
        self,
        *names_as_args: str,
        names: ty.Optional[ty.Set[str]] = None,
        prefixes: ty.Optional[ty.Set[str]] = None,
        routing_re_flags: re.RegexFlag = re.IGNORECASE,
        allow_regexes: bool = False,
        filter: ty.Optional[Filter] = None
    ) -> ty.Callable[[DecoratorFunction], Command[DecoratorFunction]]:
        def wrapper(func):
            command = Command(
                handler=func,
                names=set(names_as_args) or names,
                prefixes=prefixes,
                routing_re_flags=routing_re_flags,
                allow_regexes=allow_regexes,
                filter=filter,
            )
            self.commands.append(command)
            return command
        return wrapper

    def on_event(
        self, *event_types: EventType
    ) -> ty.Callable[[DecoratorFunction], DecoratorFunction]:
        def wrapper(func):
            for event_type in event_types:
                self.event_handlers[event_type].append(func)
            return func
        return wrapper

    def on_startup(
        self, handler: SignalHandlerTypevar
    ) -> SignalHandlerTypevar:
        self.startup_handler = handler
        return handler

    def on_shutdown(
        self, handler: SignalHandlerTypevar
    ) -> SignalHandlerTypevar:
        self.shutdown_handler = handler
        return handler

    def add_package(self, package: Package) -> None:
        self.packages.append(package)

    async def route_event(self, new_event_storage) -> None:
        routing_coroutines = [
            package.route_event(new_event_storage)
            for package in self.packages
        ]
        routing_coroutines.append(self.handle_event(new_event_storage))
        await asyncio.gather(*routing_coroutines)

    async def handle_event(self, new_event_storage: NewEventStorage) -> None:
        handlers = self.event_handlers[new_event_storage.event.type]
        handle_coroutines = [
            handler(new_event_storage)
            for handler in handlers
        ]
        await asyncio.gather(*handle_coroutines)

    async def route_message(self, message_storage: MessageStorage):
        routing_coroutines = [
            package.handle_message(message_storage)
            for package in self.packages
        ]
        routing_coroutines.append(self.handle_message(message_storage))
        await asyncio.gather(*routing_coroutines)

    async def handle_message(self, message_storage: MessageStorage):
        handle_coroutines = [
            command.handle_message(message_storage)
            for command in self.commands
        ]
        await asyncio.gather(*handle_coroutines)
