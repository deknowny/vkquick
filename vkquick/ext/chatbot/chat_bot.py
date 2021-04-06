import re
import typing as ty

from vkquick.api import API
from vkquick.signal import SignalHandler
from vkquick.bases.events_factories import EventsFactory
from vkquick.bases.middleware import Middleware
from vkquick.bot import Bot
from vkquick.bases.easy_decorator import easy_method_decorator
from vkquick.event_handler.handler import EventHandler
from vkquick.ext.chatbot.filters.base import CommandFilter
from vkquick.ext.chatbot.filters.command.command import Command
from vkquick.ext.chatbot.middlewares import MakeMessageProviderOnNewMessage


class ChatBot(Bot):

    def __init__(
        self,
        *,
        api: API,
        events_factory: ty.Optional[EventsFactory] = None,
        commands: ty.Optional[ty.List[Command]] = None,
        event_handlers: ty.Optional[ty.List[EventHandler]] = None,
        signals: ty.Optional[ty.Dict[str, SignalHandler]] = None,
        middlewares: ty.Optional[ty.List[Middleware]] = None,
    ) -> None:
        Bot.__init__(
            self,
            api=api,
            events_factory=events_factory,
            event_handlers=event_handlers,
            signals=signals,
            middlewares=middlewares
        )
        self._event_handlers.extend(commands or [])
        self._middlewares.append(MakeMessageProviderOnNewMessage())


    @easy_method_decorator
    def add_command(
        self,
        __handler: ty.Optional[ty.Callable[..., ty.Awaitable]] = None,
        *,
        names: ty.Optional[ty.Set[str]] = None,
        prefixes: ty.Optional[ty.Set[str]] = None,
        allow_regex: bool = False,
        routing_re_flags: re.RegexFlag = re.IGNORECASE,
        previous_filters: ty.Optional[ty.List[CommandFilter]] = None,
    ) -> Command:
        if not isinstance(__handler, Command):
            __handler = Command(
                __handler,
                names=names,
                prefixes=prefixes,
                allow_regex=allow_regex,
                routing_re_flags=routing_re_flags,
                previous_filters=previous_filters
            )

        self._event_handlers.append(__handler)
        return __handler
