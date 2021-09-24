from __future__ import annotations

import asyncio
import collections
import dataclasses
import re
import typing

from vkquick.base.event import EventType
from vkquick.chatbot.base.cutter import InvalidArgumentConfig
from vkquick.chatbot.base.filter import BaseFilter
from vkquick.chatbot.base.handler_container import HandlerMixin
from vkquick.chatbot.command.command import Command
from vkquick.chatbot.command.cutters import UserID, PageID
from vkquick.chatbot.exceptions import StopCurrentHandling
from vkquick.chatbot.storages import (
    CallbackButtonPressed,
    NewEvent,
    NewMessage,
)
from vkquick.chatbot.ui_builders.button import (
    ButtonCallbackHandler,
    ButtonOnclickHandler,
)

unset = object()


@dataclasses.dataclass
class MessageHandler(
    HandlerMixin[typing.Callable[[NewMessage], typing.Awaitable]]
):
    filter: typing.Optional[BaseFilter] = None

    async def run_handling(self, ctx: NewMessage):
        if self.filter is not None:
            try:
                await self.filter.run_making_decision(ctx)
            except StopCurrentHandling:
                return
        await self.handler(ctx)


class UserAddedHandler(
    HandlerMixin[
        # Context, New member, Inviter,
        typing.Callable[[NewMessage, PageID, UserID], typing.Awaitable]
    ]
):
    async def run_handling(self, ctx: NewMessage):
        if (
            ctx.msg.action is not None
            and ctx.msg.action["type"] == "chat_invite_user"
            and ctx.msg.from_id
            != int(
                invited_user := (
                    ctx.msg.action.get("member_id")
                    or ctx.msg.action.get("source_mid")
                )
            )
        ):
            await self.handler(
                ctx, PageID(invited_user), UserID(ctx.msg.from_id)
            )


class UserJoinedByLinkHandler(
    HandlerMixin[
        typing.Callable[[NewMessage, UserID], typing.Awaitable]
    ]
):
    async def run_handling(self, ctx: NewMessage):
        if (
            ctx.msg.action is not None
            and ctx.msg.action["type"] == "chat_invite_user_by_link"
        ):
            await self.handler(ctx, UserID(ctx.msg.from_id))


class UserReturnedHandler(
    HandlerMixin[
        typing.Callable[[NewMessage, UserID], typing.Awaitable]
    ]
):
    async def run_handling(self, ctx: NewMessage):
        if (
                ctx.msg.action is not None
                and ctx.msg.action["type"] == "chat_invite_user"
                and ctx.msg.from_id
                == int(
                    ctx.msg.action.get("member_id")
                    or ctx.msg.action.get("source_mid")
                )
        ):

            await self.handler(
                ctx, UserID(ctx.msg.from_id)
            )


class SignalHandler(HandlerMixin[typing.Callable[["Bot"], typing.Awaitable]]):
    pass


class EventHandler(
    HandlerMixin[typing.Callable[[NewEvent], typing.Awaitable]]
):
    pass


if typing.TYPE_CHECKING:  # pragma: no cover

    from vkquick.types import DecoratorFunction

    SignalHandlerTypevar = typing.TypeVar(
        "SignalHandlerTypevar", bound=SignalHandler
    )
    EventHandlerTypevar = typing.TypeVar(
        "EventHandlerTypevar", bound=EventHandler
    )
    MessageHandlerTypevar = typing.TypeVar(
        "MessageHandlerTypevar", bound=MessageHandler
    )


@dataclasses.dataclass
class Package:
    prefixes: typing.List[str] = dataclasses.field(default_factory=list)
    filter: typing.Optional[BaseFilter] = None
    commands: typing.List[Command] = dataclasses.field(default_factory=list)
    event_handlers: typing.Dict[
        EventType, typing.List[EventHandler]
    ] = dataclasses.field(
        default_factory=lambda: collections.defaultdict(list)
    )
    message_handlers: typing.List[MessageHandler] = dataclasses.field(
        default_factory=list
    )
    startup_handlers: typing.List[SignalHandler] = dataclasses.field(
        default_factory=list
    )
    shutdown_handlers: typing.List[SignalHandler] = dataclasses.field(
        default_factory=list
    )
    button_onclick_handlers: typing.Dict[
        str, ButtonOnclickHandler
    ] = dataclasses.field(default_factory=dict)

    button_callback_handlers: typing.Dict[
        str, ButtonCallbackHandler
    ] = dataclasses.field(default_factory=dict)

    inviting_handlers: typing.List[
        typing.Union[UserReturnedHandler, UserJoinedByLinkHandler, UserAddedHandler]
    ] = dataclasses.field(default_factory=list)

    def on_returned_user(self) -> typing.Callable[[DecoratorFunction], Command[DecoratorFunction]]:
        def wrapper(func):
            self.inviting_handlers.append(
                UserReturnedHandler(func)
            )
            return func

        return wrapper

    def on_user_joined_by_link(self) -> typing.Callable[[DecoratorFunction], Command[DecoratorFunction]]:
        def wrapper(func):
            self.inviting_handlers.append(
                UserJoinedByLinkHandler(func)
            )
            return func

        return wrapper

    def on_added_page(self) -> typing.Callable[[DecoratorFunction], Command[DecoratorFunction]]:
        def wrapper(func):
            self.inviting_handlers.append(
                UserAddedHandler(func)
            )
            return func

        return wrapper

    def command(
        self,
        *names: str,
        prefixes: typing.List[str] = None,
        routing_re_flags: typing.Union[re.RegexFlag, int] = re.IGNORECASE,
        exclude_from_autodoc: bool = False,
        filter: typing.Optional[BaseFilter] = None,
        description: typing.Optional[str] = None,
        invalid_argument_config: typing.Optional[
            InvalidArgumentConfig
        ] = unset,
    ) -> typing.Callable[[DecoratorFunction], Command[DecoratorFunction]]:
        def wrapper(func):
            command_init_vars = dict(
                handler=func,
                names=list(names),
                prefixes=prefixes or self.prefixes,
                routing_re_flags=routing_re_flags,
                exclude_from_autodoc=exclude_from_autodoc,
                filter=filter,
                description=description,
            )
            if invalid_argument_config != unset:
                command_init_vars.update(
                    invalid_argument_config=invalid_argument_config
                )
            command = Command(**command_init_vars)
            self.commands.append(command)
            return command

        return wrapper

    def on_clicked_button(
        self,
    ) -> typing.Callable[[DecoratorFunction], ButtonOnclickHandler]:
        def wrapper(func):
            if isinstance(func, Command):
                func = func.handler
            handler = ButtonOnclickHandler(func)
            self.button_onclick_handlers[func.__name__] = handler
            return handler

        return wrapper

    def on_called_button(
        self,
    ) -> typing.Callable[[DecoratorFunction], ButtonCallbackHandler]:
        def wrapper(func):
            if isinstance(func, Command):
                func = func.handler
            handler = ButtonCallbackHandler(func)
            self.button_callback_handlers[func.__name__] = handler
            return handler

        return wrapper

    def on_event(
        self, *event_types: EventType
    ) -> typing.Callable[[EventHandlerTypevar], EventHandlerTypevar]:
        def wrapper(func):
            for event_type in event_types:
                handler = EventHandler(func)
                self.event_handlers[event_type].append(handler)
            return func

        return wrapper

    def on_message(
        self, filter: typing.Optional[BaseFilter] = None
    ) -> typing.Callable[[MessageHandlerTypevar], MessageHandlerTypevar]:
        def wrapper(func):
            handler = MessageHandler(handler=func, filter=filter)
            self.message_handlers.append(handler)
            return func

        return wrapper

    def on_startup(
        self,
    ) -> typing.Callable[[SignalHandlerTypevar], SignalHandlerTypevar]:
        def wrapper(func):
            handler = SignalHandler(func)
            self.startup_handlers.append(handler)
            return func

        return wrapper

    def on_shutdown(
        self,
    ) -> typing.Callable[[SignalHandlerTypevar], SignalHandlerTypevar]:
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

    async def handle_message(self, ctx: NewMessage):
        if self.filter is not None:
            try:
                await self.filter.run_making_decision(ctx)
            except StopCurrentHandling:
                return
        command_coroutines = [
            command.handle_message(ctx) for command in self.commands
        ]
        message_handler_coroutines = [
            message_handler.run_handling(ctx)
            for message_handler in self.message_handlers
        ]
        inviting_handler_coroutines = [
            inviting_handler.run_handling(ctx)
            for inviting_handler in self.inviting_handlers
        ]
        await asyncio.gather(
            self.routing_payload(ctx),
            *command_coroutines,
            *message_handler_coroutines,
            *inviting_handler_coroutines
        )

    async def routing_payload(self, ctx: NewMessage):
        if (
            ctx.msg.payload is not None
            and ctx.msg.payload.get("command") in self.button_onclick_handlers
        ):
            handler_name = ctx.msg.payload.get("command")
            extra_arguments = {}
            if "args" in ctx.msg.payload:
                extra_arguments = ctx.msg.payload.get("args")
                if isinstance(extra_arguments, list):
                    extra_arguments = {}
            handler = self.button_onclick_handlers[handler_name]
            if NewMessage in handler.handler.__annotations__.values():
                response = await handler.handler(ctx, **extra_arguments)
            else:
                response = await handler.handler(**extra_arguments)
            if response is not None:
                await ctx.reply(str(response))

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
            if (
                CallbackButtonPressed
                in handler.handler.__annotations__.values()
            ):
                response = await handler.handler(ctx, **extra_arguments)
            else:
                response = await handler.handler(**extra_arguments)
            if response is not None:
                await ctx.show_snackbar(str(response))
