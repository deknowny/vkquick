import inspect
import re
import typing as ty
import warnings

import typing_extensions as tye

from vkquick.bases.easy_decorator import EasyDecorator, easy_class_decorator
from vkquick.event_handler.context import EventHandlingContext
from vkquick.event_handler.handler import EventHandler
from vkquick.exceptions import FilterFailedError
from vkquick.ext.chatbot.command.context import Context
from vkquick.ext.chatbot.command.statuses import (
    CommandStatus,
    IncorrectArgument,
    MissedArgument,
    NotRouted,
    UnexpectedArgument,
)
from vkquick.ext.chatbot.command.text_cutters.base import (
    Argument,
    CommandTextArgument,
    TextCutter,
)
from vkquick.ext.chatbot.command.text_cutters.cutters import (
    EntityCutter,
    FloatCutter,
    GroupCutter,
    GroupID,
    ImmutableSequenceCutter,
    IntegerCutter,
    LiteralCutter,
    Mention,
    MentionCutter,
    MutableSequenceCutter,
    OptionalCutter,
    PageID,
    StringCutter,
    UnionCutter,
    UniqueImmutableSequenceCutter,
    UniqueMutableSequenceCutter,
    UserID,
    WordCutter,
)
from vkquick.ext.chatbot.exceptions import BadArgumentError
from vkquick.ext.chatbot.filters import CommandFilter
from vkquick.ext.chatbot.providers.page import (
    GroupProvider,
    PageProvider,
    UserProvider,
)
from vkquick.ext.chatbot.wrappers.page import Group, Page, User


class CommandHandlerType1(ty.Protocol):
    async def __call__(self, ctx: Context, *args: type, **kwargs: type):
        ...


class CommandHandlerType2(ty.Protocol):
    async def __call__(self, **kwargs):
        ...


@easy_class_decorator
class Command(EventHandler, CommandFilter, EasyDecorator):

    context_factory = Context

    accepted_event_types = frozenset({"message_new", "message_reply", 4})

    def __init__(
        self,

        names: ty.Optional[ty.Set[str]] = None,
        allow_regex: bool = False,
        routing_re_flags: re.RegexFlag = re.IGNORECASE,
        afterword_filters: ty.Optional[ty.List[CommandFilter]] = None,
        foreword_filters: ty.Optional[ty.List[CommandFilter]] = None,
    ) -> None:
        self._names = names or set()
        self._names.update(names_as_args)
        self._allow_regex = allow_regex
        self._routing_re_flags = routing_re_flags

        self._text_arguments: ty.List[CommandTextArgument] = []
        self._ctx_argument_name: ty.Optional[str] = None

        self._build_routing_regex()

        afterword_filters = afterword_filters or []
        foreword_filters = foreword_filters or []

        filters = [*afterword_filters, self, *foreword_filters]

        EventHandler.__init__(
            self,
            handling_event_types=set(self.accepted_event_types),
            filters=filters,
        )

        self._parse_handler_arguments()

    def _init_handler_kwargs(self, ctx: Context) -> ty.Mapping:
        function_arguments = ctx.extra["text_arguments"].copy()
        if self._ctx_argument_name is not None:
            function_arguments[self._ctx_argument_name] = ctx

        return function_arguments

    def _init_handler_args(self, ehctx: EventHandlingContext) -> ty.Sequence:
        return ()

    async def _call_handler(self, ctx: Context, args, kwargs) -> ty.Any:
        func_response = await EventHandler._call_handler(
            self, ctx, args, kwargs
        )
        if func_response is not None:
            await ctx.mp.reply(func_response)

    async def make_decision(self, ctx: Context) -> None:
        matched_routing = self._command_routing_regex.match(
            ctx.mp.storage.text
        )
        if matched_routing is None:
            raise FilterFailedError(
                "Routing isn't matched",
                extra={
                    "status": CommandStatus.NOT_ROUTED,
                    "payload:": NotRouted(),
                },
            )
        else:
            # Make text arguments
            ctx.extra["text_arguments"] = {}
            remain_string = ctx.mp.storage.text[matched_routing.end() :]
            await self._parse_arguments(ctx, remain_string=remain_string)

    async def _parse_arguments(
        self, ctx: Context, remain_string: str
    ) -> None:
        for argtype in self._text_arguments:
            remain_string = remain_string.lstrip()
            try:
                parsing_response = await argtype.cutter.cut_part(
                    ctx, remain_string
                )
            except BadArgumentError as err:
                if not remain_string:
                    raise FilterFailedError(
                        "Missed an argument",
                        extra={
                            "status": CommandStatus.MISSED_ARGUMENT,
                            "payload:": MissedArgument(
                                command_argument=argtype,
                                remain_string=remain_string,
                            ),
                        },
                    )
                raise FilterFailedError(
                    "Incorrect argument value",
                    extra={
                        "status": CommandStatus.INCORRECT_ARGUMENT,
                        "payload:": IncorrectArgument(
                            command_argument=argtype,
                            remain_string=remain_string,
                            parsing_error=err,
                        ),
                    },
                ) from err

            else:
                remain_string = parsing_response.new_arguments_string.lstrip()
                ctx.extra["text_arguments"][
                    argtype.argument_name
                ] = parsing_response.parsed_part

        if remain_string:
            raise FilterFailedError(
                "Got unexpected argument",
                extra={
                    "status": CommandStatus.UNEXPECTED_ARGUMENT,
                    "payload:": UnexpectedArgument(
                        remain_string=remain_string
                    ),
                },
            )

    def _parse_handler_arguments(self):
        parameters = inspect.signature(self.handler).parameters
        for name, argument in parameters.items():
            if argument.annotation is Context:
                self._ctx_argument_name = argument.name
                if self._text_arguments:
                    warnings.warn(
                        "Set `CommandContext` argument the first "
                        "in the function (style recommendation)"
                    )

            else:
                text_argument = _resolve_typing(argument)
                self._text_arguments.append(text_argument)

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
            prefixes = {re.escape(prefix) for prefix in self._prefixes}
            names = {re.escape(name) for name in self._names}

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
