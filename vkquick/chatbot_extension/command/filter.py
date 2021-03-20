from __future__ import annotations

import inspect
import re
import typing as ty

from loguru import logger

from vkquick.bases.filter import Filter
from vkquick.bases.easy_decorator import EasyDecorator
from vkquick.event_handler.context import EventHandlingContext
from vkquick.chatbot_extension.command.context import CommandContext
from vkquick.event import GroupEvent
from vkquick.chatbot_extension.text_cutters.base import (
    TextCutter,
)
from vkquick.chatbot_extension.command.statuses import (
    CommandValidatingStatus,
    RoutingUnmatched
)
from vkquick.exceptions import FilterFailedError
from vkquick.chatbot_extension.wrappers.message import Message

if ty.TYPE_CHECKING:
    pass


class CommandFilter(Filter, EasyDecorator):

    __accepted_event_types__ = frozenset({4, "message_new"})

    def __init__(
        self,
        __handler: ty.Optional[ty.Callable] = None,
        *,
        prefixes: ty.Optional[ty.Set[str]] = None,
        names: ty.Optional[ty.Set[str]] = None,
        use_regex_escape: bool = True,
        routing_command_re_flags: re.RegexFlag = re.IGNORECASE,
    ):
        self._handler = __handler
        self._names = prefixes or set()
        self._prefixes = names or set()
        self._use_regex_escape = use_regex_escape
        self._routing_command_re_flags = routing_command_re_flags
        self._command_routing_regex = self._build_routing_regex()

        self._text_cutters: ty.List[ty.Tuple[str, TextCutter]] = []
        self._command_context_name: ty.Optional[str] = None

        self._resolve_arguments()

    async def make_decision(self, ehctx: EventHandlingContext):
        message = await _fetch_wrapped_message(ehctx)
        ctx = CommandContext(ehctx=ehctx, message=message)


    @logger.catch(reraise=True)
    def _validate_routing_regex(self, ctx: CommandContext):
        routing_match = self._command_routing_regex.match(ctx.msg.text)
        if routing_match is None:
            raise FilterFailedError(
                self, "Routing doesn't match",
                command_context=ctx
            )

    def _resolve_arguments(self) -> None:
        """
        Вызывается в момент декорирования для распознания того,
        какие аргументы следует передавать в реакцию
        """
        parameters = inspect.signature(self._handler).parameters
        parameters = list(parameters.items())
        for name, value in parameters:
            if name == "ctx" or value.annotation is CommandContext:
                self._command_context_name = name
            elif inspect.isclass(value.annotation) and issubclass(
                value.annotation, TextCutter
            ):
                self._text_cutters.append((name, value.annotation()))
            elif isinstance(value.annotation, TextCutter):
                self._text_cutters.append((name, value.annotation))

    def _build_routing_regex(self) -> re.Pattern:
        """
        Выстраивает регулярное выражение, по которому
        определяется вызов команды. Не включает в себя
        аргументы, т.к. для них задается своя логика фильтром
        """
        # Экранирование специальных символов, если такое указано
        if self._use_regex_escape:
            prefixes = map(re.escape, self._prefixes)
            names = map(re.escape, self._names)
        else:
            prefixes = self._prefixes
            names = self._names

        # Объединение имен и префиксов через или
        self._prefixes_regex = "|".join(prefixes)
        self._names_regex = "|".join(names)

        # Проверка длины, чтобы не создавать лишние группы
        if len(self._prefixes) > 1:
            self._prefixes_regex = f"(?:{self._prefixes_regex})"
        if len(self._names) > 1:
            self._names_regex = f"(?:{self._names_regex})"

        return re.compile(
            self._prefixes_regex + self._names_regex,
            flags=self._routing_command_re_flags,
        )


def _call_with_optional_context(func, context: Context):
    parameters = inspect.signature(func).parameters
    if len(parameters) == 1:
        return func(context)
    elif len(parameters) == 0:
        return func()


async def _optional_call_with_autoreply(func, context: Context):
    if isinstance(func, str):
        response = func
    else:
        response = await sync_async_run(
            _call_with_optional_context(func, context)
        )
    if response is not None:
        await context.reply(response)


async def _fetch_wrapped_message(ehctx: EventHandlingContext) -> Message:
    if isinstance(ehctx.event, GroupEvent):
        message_raw = ehctx.event.object
        # Для LongPoll ^5.103
        if "message" in message_raw:
            message_raw = message_raw["message"]

        message = Message(message_raw)

    else:
        message_raw = await ehctx.api.messages.get_by_id(
            ..., message_ids=ehctx.event.content[1]
        )
        message = Message(message_raw["items"][0])

    return message
