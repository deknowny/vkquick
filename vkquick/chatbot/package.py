from __future__ import annotations

import asyncio
import collections
import dataclasses
import re
import typing as ty

from vkquick.base.event import EventType
from vkquick.chatbot.base.filter import BaseFilter
from vkquick.chatbot.base.handler_container import HandlerMixin
from vkquick.chatbot.command.command import Command
from vkquick.chatbot.exceptions import FilterFailedError
from vkquick.chatbot.storages import (
    CallbackButtonPressed,
    NewEvent,
    NewMessage,
)
from vkquick.chatbot.ui_builders.button import (
    ButtonCallbackHandler,
    ButtonOnclickHandler,
)


@dataclasses.dataclass
class MessageHandler(HandlerMixin):
    handler: ty.Callable[[NewMessage], ty.Awaitable]


@dataclasses.dataclass
class SignalHandler(HandlerMixin):
    handler: ty.Callable[[Bot], ty.Awaitable]


@dataclasses.dataclass
class EventHandler(HandlerMixin):
    handler: ty.Callable[[NewEvent], ty.Awaitable]


if ty.TYPE_CHECKING:

    from vkquick.chatbot.application import Bot
    from vkquick.types import DecoratorFunction

    SignalHandlerTypevar = ty.TypeVar(
        "SignalHandlerTypevar", bound=SignalHandler
    )
    EventHandlerTypevar = ty.TypeVar(
        "EventHandlerTypevar", bound=EventHandler
    )
    MessageHandlerTypevar = ty.TypeVar(
        "MessageHandlerTypevar", bound=MessageHandler
    )


@dataclasses.dataclass
class Package:
    prefixes: ty.List[str] = dataclasses.field(default_factory=list)
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
    button_onclick_handlers: ty.Dict[
        str, ButtonOnclickHandler
    ] = dataclasses.field(default_factory=dict)

    button_callback_handlers: ty.Dict[
        str, ButtonCallbackHandler
    ] = dataclasses.field(default_factory=dict)

    def command(
        self,
        *names: str,
        prefixes: ty.List[str] = None,
        routing_re_flags: re.RegexFlag = re.IGNORECASE,
        exclude_from_autodoc: bool = False,
        filter: ty.Optional[BaseFilter] = None
    ) -> ty.Callable[[DecoratorFunction], Command[DecoratorFunction]]:
        def wrapper(func):
            command = Command(
                handler=func,
                names=list(names),
                prefixes=prefixes or self.prefixes,
                routing_re_flags=routing_re_flags,
                exclude_from_autodoc=exclude_from_autodoc,
                filter=filter,
            )
            self.commands.append(command)
            return command

        return wrapper

    def on_clicked_button(
        self,
    ) -> ty.Callable[[DecoratorFunction], ButtonOnclickHandler]:
        def wrapper(func):
            if isinstance(func, Command):
                func = func.handler
            handler = ButtonOnclickHandler(func)
            self.button_onclick_handlers[func.__name__] = handler
            return handler

        return wrapper

    def on_called_button(
        self,
    ) -> ty.Callable[[DecoratorFunction], ButtonCallbackHandler]:
        def wrapper(func):
            if isinstance(func, Command):
                func = func.handler
            handler = ButtonCallbackHandler(func)
            self.button_callback_handlers[func.__name__] = handler
            return handler

        return wrapper

    def on_event(
        self, *event_types: EventType
    ) -> ty.Callable[[EventHandlerTypevar], EventHandlerTypevar]:
        def wrapper(func):
            for event_type in event_types:
                handler = EventHandler(func)
                self.event_handlers[event_type].append(handler)
            return func

        return wrapper

    def on_message(
        self,
    ) -> ty.Callable[[MessageHandlerTypevar], MessageHandlerTypevar]:
        def wrapper(func):
            handler = MessageHandler(func)
            self.message_handlers.append(handler)
            return func

        return wrapper

    def on_startup(
        self,
    ) -> ty.Callable[[SignalHandlerTypevar], SignalHandlerTypevar]:
        def wrapper(func):
            handler = SignalHandler(func)
            self.startup_handlers.append(handler)
            return func

        return wrapper

    def on_shutdown(
        self,
    ) -> ty.Callable[[SignalHandlerTypevar], SignalHandlerTypevar]:
        def wrapper(func):
            handler = SignalHandler(func)
            self.shutdown_handlers.append(handler)
            return func

        return wrapper

    async def handle_event(self, new_event_storage: NewEvent) -> None:
        handlers = self.event_handlers[new_event_storage.event.type]
        handle_coroutines = [
            handler.handler(new_event_storage) for handler in handlers
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
            message_handler.handler(message_storage)
            for message_handler in self.message_handlers
        ]
        await asyncio.gather(
            self.routing_payload(message_storage),
            *command_coroutines,
            *message_handler_coroutines
        )

    async def routing_payload(self, message_storage: NewMessage):
        if (
            message_storage.msg.payload is not None
            and message_storage.msg.payload.get("command")
            in self.button_onclick_handlers
        ):
            handler_name = message_storage.msg.payload.get("command")
            extra_arguments = {}
            if "args" in message_storage.msg.payload:
                extra_arguments = message_storage.msg.payload.get("args")
            handler = self.button_onclick_handlers[handler_name]
            if NewMessage in handler.handler.__annotations__.values():
                response = await handler.handler(
                    message_storage, **extra_arguments
                )
            else:
                response = await handler.handler(**extra_arguments)
            if response is not None:
                await message_storage.reply(str(response))

    async def handle_callback_button_pressing(
        self, ctx: CallbackButtonPressed
    ):
        if (
            ctx.msg.payload is not None
            and ctx.msg.payload.get("command")
            in self.button_callback_handlers
        ):
            handler_name = ctx.msg.payload.get("command")
            extra_arguments = {}
            if "args" in ctx.msg.payload:
                extra_arguments = ctx.msg.payload.get("args")
                # Я тебя ненавижу, апи вконтукте
                if isinstance(extra_arguments, list):
                    extra_arguments = {}
            handler = self.button_callback_handlers[handler_name]
            if NewMessage in handler.handler.__annotations__.values():
                response = await handler.handler(ctx, **extra_arguments)
            else:
                response = await handler.handler(**extra_arguments)
            if response is not None:
                await ctx.show_snackbar(str(response))
