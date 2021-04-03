import inspect
import re
import typing as ty
import warnings

from vkquick.bases.filter import Filter
from vkquick.event_handler.context import EventHandlingContext
from vkquick.event_handler.handler import EventHandler
from vkquick.exceptions import ExpectedMiddlewareToBeUsed
from vkquick.ext.chatbot.filters.command.text_cutters.base import TextCutter
from vkquick.ext.chatbot.filters.command.text_cutters.integer import Integer
from vkquick.ext.chatbot.providers.message import MessageProvider


def _resolve_typing(parameter: inspect.Parameter):
    if typing_type is int:
        return Integer()


class Command(Filter, EventHandler):

    __accepted_event_types__ = frozenset({"message_new", 4})

    def __init__(
        self,
        __handler: ty.Optional[ty.Callable[..., ty.Awaitable]] = None,
        *,
        names: ty.Optional[ty.Set[str]] = None,
        prefixes: ty.Optional[ty.Set[str]] = None,
        allow_regex: bool = False,
        routing_re_flags: re.RegexFlag = re.IGNORECASE,
        previous_filters: ty.Optional[ty.List[Filter]] = None,
    ) -> None:
        self._names = names
        self._prefixes = prefixes
        self._allow_regex = allow_regex
        self._routing_re_flags = routing_re_flags

        self._text_arguments: ty.List[ty.Tuple[str, TextCutter]] = []
        self._message_provider_argument_name: ty.Optional[str] = None
        self._ehctx_argument_name: ty.Optional[str] = None

        self._build_routing_regex()

        if previous_filters is None:
            previous_filters = [self]
        else:
            previous_filters.append(self)

        EventHandler.__init__(
            self,
            __handler,
            handling_event_types=self.__accepted_event_types__,
            filters=previous_filters,
        )

    def __call__(self, event_handler: EventHandler) -> EventHandler:
        self._handler = event_handler.handler
        self._parse_handler_arguments()
        return super().__call__(event_handler)

    async def make_decision(self, ehctx: EventHandlingContext) -> None:
        try:
            ehctx.epctx.extra["cultivated_message"]
        except KeyError as err:
            raise ExpectedMiddlewareToBeUsed(
                "MakeMessageProviderOnNewMessage"
            ) from err

    def _parse_handler_arguments(self):
        parameters = inspect.signature(self._handler).parameters
        for name, argument in parameters.items():
            if argument.annotation is MessageProvider:
                self._message_provider_argument_name = argument.name
                # if self._text_arguments:
                #     warnings.warn(
                #         "Use MessageProvider argument the first "
                #         "in the function (style recommendation)"
                #     )
            elif argument.annotation is EventHandlingContext:
                self._ehctx_argument_name = argument.name
                ...

    def _build_routing_regex(self) -> None:
        """
        Выстраивает регулярное выражение, по которому
        определяется вызов команды. Не включает в себя
        аргументы, т.к. для них задается своя логика фильтром
        """
        # Экранирование специальных символов, если такое указано
        if self._allow_regex:
            prefixes = self._prefixes
            names = self._names

        else:
            prefixes = map(re.escape, self._prefixes)
            names = map(re.escape, self._names)

        # Объединение имен и префиксов через или
        prefixes_regex = "|".join(prefixes)
        names_regex = "|".join(names)

        # Проверка длины, чтобы не создавать лишние группы
        if len(self._prefixes) > 1:
            prefixes_regex = f"(?:{prefixes_regex})"
        if len(self._names) > 1:
            names_regex = f"(?:{names_regex})"

        self._command_routing_regex = re.compile(
            prefixes_regex + names_regex,
            flags=self._routing_re_flags,
        )
