import inspect
import re
import types
import typing as ty
import warnings

from vkquick.bases.easy_decorator import EasyDecorator
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
    FloatCutter,
    IntegerCutter,
    OptionalCutter,
    StringCutter,
    WordCutter, UnionCutter,
)
from vkquick.ext.chatbot.exceptions import BadArgumentError
from vkquick.ext.chatbot.filters import CommandFilter
from vkquick.ext.chatbot.providers.message import MessageProvider


def _resolve_typing(parameter: inspect.Parameter) -> CommandTextArgument:
    if isinstance(parameter.default, Argument):
        arg_settings = parameter.default
    elif parameter.default != parameter.empty:
        arg_settings = Argument(default=parameter.default)
    else:
        arg_settings = Argument()

    if (
        arg_settings.default is not None
        or arg_settings.default_factory is not None
        and not isinstance(parameter.annotation, OptionalCutter)
    ):
        arg_annotation = ty.Optional[parameter.annotation]
    else:
        arg_annotation = parameter.annotation

    cutter = _resolve_cutter(
        arg_name=parameter.name,
        arg_annotation=arg_annotation,
        arg_settings=arg_settings,
        arg_kind=parameter.kind,
    )
    return CommandTextArgument(
        argument_name=parameter.name,
        argument_settings=arg_settings,
        cutter=cutter,
    )


def _resolve_cutter(
    *, arg_name: str, arg_annotation: ty.Any, arg_settings: Argument, arg_kind
) -> TextCutter:

    if arg_annotation is int:
        return IntegerCutter()
    elif arg_annotation is float:
        return FloatCutter()
    elif arg_annotation is str:
        if arg_kind == inspect.Parameter.KEYWORD_ONLY:
            return StringCutter()
        else:
            return WordCutter()

    # Optional
    elif (
        arg_annotation.__class__ is ty._GenericAlias  # noqa
        and ty.get_origin(arg_annotation) is ty.Union
        and type(None) in ty.get_args(arg_annotation)
    ):
        return OptionalCutter(
            default=arg_settings.default,
            default_factory=arg_settings.default_factory,
            typevars=[
                _resolve_cutter(
                    arg_name=arg_name,
                    arg_annotation=ty.get_args(arg_annotation)[0],
                    arg_settings=arg_settings,
                    arg_kind=arg_kind,
                )
            ],
        )
    # Union
    elif (
        arg_annotation.__class__ is ty._GenericAlias  # noqa
        and ty.get_origin(arg_annotation) is ty.Union
    ):
        typevar_cutters = [
            _resolve_cutter(
                arg_name=arg_name,
                arg_annotation=typevar,
                arg_settings=arg_settings,
                arg_kind=arg_kind,
            )
            for typevar in ty.get_args(arg_annotation)
        ]
        return UnionCutter(
            typevars=typevar_cutters
        )
    else:
        raise TypeError(f"Can't resolve cutter from argument `{arg_name}`")


class Command(EventHandler, CommandFilter, EasyDecorator):

    context_factory = Context

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

    def _init_handler_kwargs(self, ctx: Context) -> ty.Mapping:
        function_arguments = ctx.extra["text_arguments"].copy()
        if self._ctx_argument_name is not None:
            function_arguments[self._ctx_argument_name] = ctx
        if self._message_provider_argument_name is not None:
            function_arguments[self._message_provider_argument_name] = ctx.mp

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
            if argument.annotation is Context:
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
