import inspect
import re
import types
import typing as ty
import warnings

from vkquick.exceptions import FilterFailedError
from vkquick.event_handler.context import EventHandlingContext
from vkquick.event_handler.handler import EventHandler
from vkquick.ext.chatbot.exceptions import BadArgumentError
from vkquick.ext.chatbot.filters.base import CommandFilter
from vkquick.ext.chatbot.filters.command.statuses import (
    CommandStatus,
    NotRouted,
    IncorrectArgument,
    UnexpectedArgument,
    MissedArgument,
)
from vkquick.ext.chatbot.filters.command.text_cutters.base import (
    TextCutter,
    CommandTextArgument,
    Argument,
)
from vkquick.ext.chatbot.filters.command.text_cutters.cutters import (
    IntegerCutter,
    FloatCutter,
    WordCutter,
    StringCutter,
    OptionalCutter,
)
from vkquick.ext.chatbot.providers.message import MessageProvider
from vkquick.ext.chatbot.filters.command.context import CommandContext
from vkquick.bases.easy_decorator import EasyDecorator


def _resolve_typing(parameter: inspect.Parameter) -> CommandTextArgument:
    arg_name = parameter.name
    if (
        not isinstance(parameter.default, Argument)
        and parameter.default != parameter.empty
    ):
        arg_settings = Argument(default=parameter.default)
        arg_cutter = _resolve_cutter(
            arg_settings, parameter.annotation, parameter
        )
        if not isinstance(arg_cutter, OptionalCutter):
            arg_cutter = OptionalCutter(
                default=arg_settings.default, generic_types=[arg_cutter]
            )
    else:
        arg_settings = parameter.default
        if arg_settings == parameter.empty:
            arg_settings = Argument()
        if arg_settings.cutter is None:
            arg_cutter = _resolve_cutter(
                arg_settings, parameter.annotation, parameter
            )
        else:
            arg_cutter = arg_settings.cutter

    return CommandTextArgument(
        argument_name=arg_name,
        argument_settings=arg_settings,
        cutter=arg_cutter,
    )


def _resolve_cutter(
    argument_settings: Argument, argtype: ty.Any, parameter: inspect.Parameter
) -> TextCutter:
    if argtype is int:
        return IntegerCutter()
    elif argtype is float:
        return FloatCutter()
    elif argtype is str:
        if parameter.kind == parameter.KEYWORD_ONLY:
            return StringCutter()
        else:
            return WordCutter()

    # GenericAlias
    elif "__origin__" in dir(argtype):
        if argtype.__origin__ is ty.Union:
            none_type = type(None)
            if none_type in argtype.__args__:
                return OptionalCutter(
                    default=argument_settings.default,
                    default_factory=argument_settings.default_factory,
                    generic_types=[
                        _resolve_cutter(
                            argument_settings, argtype.__args__[0], parameter
                        )
                    ],
                )

    else:
        raise TypeError(f"Can't resolve cutter from parameter {parameter}")


class Command(EventHandler, CommandFilter, EasyDecorator):

    context_factory = CommandContext

    __accepted_event_types__ = frozenset({"message_new", 4})

    def __init__(
        self,
        __handler: ty.Optional[ty.Callable[..., ty.Awaitable]] = None,
        *,
        names: ty.Optional[ty.Set[str]] = None,
        prefixes: ty.Optional[ty.Set[str]] = None,
        allow_regex: bool = False,
        routing_re_flags: re.RegexFlag = re.IGNORECASE,
        previous_filters: ty.Optional[ty.List[CommandFilter]] = None,
    ) -> None:
        self._names = names or set()
        self._prefixes = prefixes or set()
        self._allow_regex = allow_regex
        self._routing_re_flags = routing_re_flags

        self._text_arguments: ty.List[CommandTextArgument] = []
        self._message_provider_argument_name: ty.Optional[str] = None
        self._ctx_argument_name: ty.Optional[str] = None

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

        self._parse_handler_arguments()

    def _init_handler_kwargs(self, ctx: CommandContext) -> ty.Mapping:
        function_arguments = ctx.extra["text_arguments"].copy()
        if self._ctx_argument_name is not None:
            function_arguments[self._ctx_argument_name] = ctx
        if self._message_provider_argument_name is not None:
            function_arguments[self._message_provider_argument_name] = ctx.mp

        return function_arguments

    def _init_handler_args(self, ehctx: EventHandlingContext) -> ty.Sequence:
        return ()

    async def _call_handler(
        self, ctx: CommandContext, args, kwargs
    ) -> ty.Any:
        func_response = await EventHandler._call_handler(
            self, ctx, args, kwargs
        )
        if func_response is not None:
            await ctx.mp.reply(func_response)

    async def make_decision(self, ctx: CommandContext) -> None:
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
        self, ctx: CommandContext, remain_string: str
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
                    "Missed an argument",
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
        parameters = inspect.signature(self._handler).parameters
        for name, argument in parameters.items():
            if argument.annotation is CommandContext:
                self._ctx_argument_name = argument.name
                if (
                    self._text_arguments
                    or self._message_provider_argument_name is not None
                ):
                    warnings.warn(
                        "Set `CommandContext` argument the first "
                        "in the function (style recommendation)"
                    )

            elif argument.annotation is MessageProvider:
                self._message_provider_argument_name = argument.name
                if self._text_arguments:
                    warnings.warn(
                        "Set `MessageProvider` argument the first "
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
