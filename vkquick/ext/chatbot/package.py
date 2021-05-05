from __future__ import annotations

import asyncio
import collections
import dataclasses
import re
import typing as ty

from vkquick.base.event import EventType
from vkquick.ext.chatbot.base.filter import BaseFilter
from vkquick.ext.chatbot.command.command import Command
from vkquick.ext.chatbot.exceptions import FilterFailedError

if ty.TYPE_CHECKING:

    from vkquick.ext.chatbot.application import Bot
    from vkquick.ext.chatbot.storages import NewEvent, NewMessage
    from vkquick.types import DecoratorFunction

    SignalHandler = ty.Callable[[Bot], ty.Awaitable]
    SignalHandlerTypevar = ty.TypeVar(
        "SignalHandlerTypevar", bound=SignalHandler
    )
    EventHandler = ty.Callable[[NewEvent], ty.Awaitable]
    EventHandlerTypevar = ty.TypeVar(
        "EventHandlerTypevar", bound=EventHandler
    )
    MessageHandler = ty.Callable[[NewMessage], ty.Awaitable]
    MessageHandlerTypevar = ty.TypeVar(
        "MessageHandlerTypevar", bound=MessageHandler
    )


@dataclasses.dataclass
class Package:
    prefixes: ty.Collection[str] = dataclasses.field(default_factory=tuple)
    filter: ty.Optional[BaseFilter] = None
    commands: ty.List[Command] = dataclasses.field(default_factory=list)
    event_handlers: ty.Dict[
        EventType, ty.List[EventHandler]
    ] = dataclasses.field(
        default_factory=lambda: collections.defaultdict(list)
    )
    message_handlers: ty.List[MessageHandler] = dataclasses.field(
        default_factory=list
    )
    startup_handlers: ty.List[SignalHandler] = dataclasses.field(
        default_factory=list
    )
    shutdown_handlers: ty.List[SignalHandler] = dataclasses.field(
        default_factory=list
    )

    def command(
        self,
        *names: str,
        prefixes: ty.Collection[str] = None,
        routing_re_flags: re.RegexFlag = re.IGNORECASE,
        enable_regexes: bool = False,
        filter: ty.Optional[BaseFilter] = None
    ) -> ty.Callable[[DecoratorFunction], Command[DecoratorFunction]]:
        def wrapper(func):
            command = Command(
                handler=func,
                names=set(names),
                prefixes=set(prefixes or self.prefixes),
                routing_re_flags=routing_re_flags,
                enable_regexes=enable_regexes,
                filter=filter,
            )
            self.commands.append(command)
            return command

        return wrapper

    def on_event(
        self, *event_types: EventType
    ) -> ty.Callable[[EventHandlerTypevar], EventHandlerTypevar]:
        def wrapper(func):
            for event_type in event_types:
                self.event_handlers[event_type].append(func)
            return func

        return wrapper

    def on_message(
        self,
    ) -> ty.Callable[[MessageHandlerTypevar], MessageHandlerTypevar]:
        def wrapper(func):
            self.message_handlers.append(func)
            return func

        return wrapper

    def on_startup(
        self, handler: SignalHandlerTypevar
    ) -> SignalHandlerTypevar:
        self.startup_handlers.append(handler)
        return handler

    def on_shutdown(
        self, handler: SignalHandlerTypevar
    ) -> SignalHandlerTypevar:
        self.shutdown_handlers.append(handler)
        return handler

    async def handle_event(self, new_event_storage: NewEvent) -> None:
        handlers = self.event_handlers[new_event_storage.event.type]
        handle_coroutines = [
            handler(new_event_storage) for handler in handlers
        ]
        await asyncio.gather(*handle_coroutines)

    async def handle_message(self, message_storage: NewMessage):
        if self.filter is not None:
            try:
                await self.filter.make_decision(message_storage)
            except FilterFailedError:
                return
        command_coroutines = [
            command.handle_message(message_storage)
            for command in self.commands
        ]
        message_handler_coroutines = [
            message_handler(message_storage)
            for message_handler in self.message_handlers
        ]
        await asyncio.gather(*command_coroutines, *message_handler_coroutines)
