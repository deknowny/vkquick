import inspect
import re
import typing as ty

import vkquick as vq

from vkquick.ext.chatbot.filters.command.context import CommandContext
from vkquick.ext.chatbot.filters.command.text_cutters.base import TextCutter
from vkquick.ext.chatbot.filters.command.text_cutters.integer import Integer


def _resolve_typing(parameter: inspect.Parameter):
    if typing_type is int:
        return Integer()


class CommandFilter(vq.Filter):

    __accepted_event_types__ = frozenset({"message_new", 4})

    def __init__(
        self,
        *,
        names: ty.Optional[ty.Set[str]] = None,
        prefixes: ty.Optional[ty.Set[str]] = None,
        allow_regex: bool = False,
        routing_re_flags: re.RegexFlag = re.IGNORECASE,
    ) -> None:
        self._names = names
        self._prefixes = prefixes
        self._allow_regex = allow_regex
        self._routing_re_flags = routing_re_flags

        self._handler: ty.Optional[vq.EventHandler] = None
        self._text_arguments: ty.List[ty.Tuple[str, TextCutter]] = []
        self._context_factory: ty.Optional[CommandContext] = None
        self._build_routing_regex()

    def __call__(self, event_handler: vq.EventHandler) -> vq.EventHandler:
        self._handler = event_handler.handler
        self._parse_handler_arguments()
        return super().__call__(event_handler)

    async def make_decision(self, ehctx: vq.EventHandlingContext) -> None:
        msg = ehctx.epctx.extra.get("")

    def _parse_handler_arguments(self):
        parameters = inspect.signature(self._handler).parameters
        for name, argument in parameters.items():
            if inspect.isclass(argument.annotation) and issubclass(
                argument.annotation, CommandContext
            ):
                self._context_factory = argument.annotation
            elif ...:
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
