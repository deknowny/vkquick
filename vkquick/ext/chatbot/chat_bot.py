import re
import typing as ty

from vkquick.api import API
from vkquick.bases.easy_decorator import easy_method_decorator
from vkquick.bases.events_factories import EventsFactory
from vkquick.bases.middleware import Middleware
from vkquick.bot import Bot
from vkquick.event_handler.handler import EventHandler
from vkquick.ext.chatbot.command.command import Command
from vkquick.ext.chatbot.filters import CommandFilter
from vkquick.ext.chatbot.middlewares import MakeMessageProviderOnNewMessage
from vkquick.signal import SignalHandler


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
            middlewares=middlewares,
        )
        self._event_handlers.extend(commands or [])
        self._middlewares.append(MakeMessageProviderOnNewMessage())

    @easy_method_decorator
    def command(
        self,
        *names_as_args: str,
        names: ty.Optional[ty.Set[str]] = None,
        prefixes: ty.Optional[ty.Set[str]] = None,
        allow_regex: bool = False,
        routing_re_flags: re.RegexFlag = re.IGNORECASE,
        afterword_filters: ty.Optional[ty.List[CommandFilter]] = None,
        foreword_filters: ty.Optional[ty.List[CommandFilter]] = None,
    ) -> Command:
        handler = Command(
            *names_as_args,
            names=names,
            prefixes=prefixes,
            allow_regex=allow_regex,
            routing_re_flags=routing_re_flags,
            afterword_filters=afterword_filters,
            foreword_filters=foreword_filters
        )
        self._event_handlers.append(handler)
        self.add_commands(handler)
        return handler

    def add_commands(self, *commands: Command) -> None:
        self._event_handlers.extend(commands)
