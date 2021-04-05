import inspect
import re
import typing as ty
import warnings

from vkquick.exceptions import FilterFailedError
from vkquick.bases.filter import Filter
from vkquick.event_handler.context import EventHandlingContext
from vkquick.event_handler.handler import EventHandler
from vkquick.ext.chatbot.exceptions import BadArgumentError
from vkquick.ext.chatbot.filters.base import CommandFilter
from vkquick.ext.chatbot.filters.command.statuses import (
    CommandStatus,
    NotRouted,
    IncorrectArgument,
    UnexpectedArgument,
    MissedArgument
)
from vkquick.ext.chatbot.filters.command.text_cutters.base import TextCutter, CommandTextArgument, Argument
from vkquick.ext.chatbot.filters.command.text_cutters.cutters import Integer
from vkquick.ext.chatbot.providers.message import MessageProvider
from vkquick.ext.chatbot.filters.command.context import CommandContext
from vkquick.bases.easy_decorator import EasyDecorator


def _resolve_typing(parameter: inspect.Parameter) -> CommandTextArgument:
    arg_name = parameter.name
    if parameter.default == parameter.empty:
        arg_settings = Argument()
    else:
        arg_settings = parameter.default

    arg_cutter = _resolve_cutter(parameter.annotation)

    return CommandTextArgument(
        argument_name=arg_name,
        argument_settings=arg_settings,
        cutter=arg_cutter
    )


def _resolve_cutter(argtype: ty.Any) -> TextCutter:
    if argtype is int:
        return Integer()


class Command(EventHandler, CommandFilter, EasyDecorator):

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

    async def make_decision(self, ctx: CommandContext) -> None:
        matched_routing = self._command_routing_regex.match(
            ctx.mp.storage.text
        )
        if matched_routing is None:
            raise FilterFailedError("Routing isn't matched", extra_payload_params={
                "status": CommandStatus.NOT_ROUTED,
                "payload:": NotRouted()
            })
        else:
            ...

    async def _parse_arguments(self, ctx: CommandContext) -> None:
        remain_string = ctx.mp.storage.text.lstrip()
        for argtype in self._text_arguments:

            remain_string = remain_string.lstrip()

            if not remain_string:
                raise FilterFailedError("Missed an argument", extra_payload_params={
                    "status": CommandStatus.MISSED_ARGUMENT,
                    "payload:": MissedArgument(command_argument=argtype, remain_string=remain_string)
                })

            try:
                parsing_response = argtype.cutter.cut_part(remain_string)
            except BadArgumentError as err:
                raise FilterFailedError("Missed an argument", extra_payload_params={
                    "status": CommandStatus.INCORRECT_ARGUMENT,
                    "payload:": IncorrectArgument(command_argument=argtype, remain_string=remain_string, parsing_error=err)
                }) from err

            else:
                remain_string = parsing_response.new_arguments_string.lstrip()
                argument_value = argtype.cutter.cast_to_type(ctx, parsing_response.parsed_part)

        if remain_string:
            raise FilterFailedError("Got unexpected argument", extra_payload_params={
                "status": CommandStatus.UNEXPECTED_ARGUMENT,
                "payload:": UnexpectedArgument(remain_string=remain_string)
            })

    async def _handle_event(self, ehctx: EventHandlingContext) -> None:
        ctx = CommandContext(
            epctx=ehctx.epctx,
            event_handler=ehctx.event_handler,
            handling_status=ehctx.handling_status,
            handling_payload=ehctx.handling_payload,
            handler_arguments=ehctx.handler_arguments,
            extra=ehctx.extra
        )
        await EventHandler._handle_event(self, ehctx=ctx)

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
            elif argument.annotation is CommandContext:
                self._ctx_argument_name = argument.name

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
