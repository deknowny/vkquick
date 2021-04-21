from __future__ import annotations

import dataclasses
import inspect
import re
import typing as ty
import warnings

from vkquick.ext.chatbot.base.cutter import TextCutter, CommandTextArgument
from vkquick.ext.chatbot.base.filter import Filter
from vkquick.ext.chatbot.command.adapters import resolve_typing
from vkquick.ext.chatbot.exceptions import BadArgumentError
from vkquick.ext.chatbot.storages import MessageStorage
from vkquick_old.exceptions import FilterFailedError

Handler = ty.TypeVar("Handler", bound=ty.Callable[..., ty.Awaitable])


@dataclasses.dataclass
class Command(ty.Generic[Handler]):
    def __init__(
        self,
        *,
        handler: Handler,
        names: ty.Optional[ty.Set[str]] = None,
        prefixes: ty.Optional[ty.Set[str]] = None,
        routing_re_flags: re.RegexFlag = re.IGNORECASE,
        allow_regexes: bool = False,
        filter: ty.Optional[Filter] = None,
    ):
        self._handler = handler
        self._names: ty.Set[str] = names or set()
        self._prefixes: ty.Set[str] = prefixes or set()
        self._routing_re_flags = routing_re_flags
        self._allow_regexes = allow_regexes
        self._filter = filter

        self._routing_regex: ty.Pattern
        self._build_routing_regex()

        self._text_arguments: ty.List[CommandTextArgument] = []
        self._message_storage_argument_name: str
        self._parse_handler_arguments()

    async def handle_message(self, message_storage: MessageStorage) -> None:
        is_routing_matched = self._routing_regex.match(message_storage.msg.text)
        if is_routing_matched:
            arguments = await self._make_arguments(
                message_storage, message_storage.msg.text[is_routing_matched.end():]
            )
            if arguments is not None:
                passed_filter = await self._run_through_filters(message_storage)
                # Were built correctly
                if passed_filter:
                    await self._call_handler(message_storage, arguments)

    async def _run_through_filters(self, message_storage: MessageStorage) -> bool:
        if self._filter is not None:
            try:
                await self._filter.make_decision(message_storage)
            except FilterFailedError:
                return False
            else:
                return True

    async def _make_arguments(
        self, message_storage: MessageStorage, arguments_string: str
    ) -> ty.Optional[ty.Dict[str, ty.Any]]:
        arguments = {}
        remain_string = arguments_string.lstrip()
        for argtype in self._text_arguments:
            remain_string = remain_string.lstrip()
            try:
                parsing_response = await argtype.cutter.cut_part(
                    message_storage, remain_string
                )
            except BadArgumentError:
                if not remain_string:
                    return None
            else:
                remain_string = parsing_response.new_arguments_string.lstrip()
                arguments[
                    argtype.argument_name
                ] = parsing_response.parsed_part

        if remain_string:
            return None

        arguments[self._message_storage_argument_name] = message_storage
        return arguments

    async def _call_handler(self, message_storage, arguments) -> None:
        handler_response = await self._handler(**arguments)
        if handler_response is not None:
            message_storage.mp.reply(handler_response)

    def _parse_handler_arguments(self) -> None:
        parameters = inspect.signature(self._handler).parameters
        for name, argument in parameters.items():
            if argument.annotation is MessageStorage:
                self._message_storage_argument_name = argument.name
                if self._text_arguments:
                    warnings.warn(
                        "Set `CommandContext` argument the first "
                        "in the function (style recommendation)"
                    )

            else:
                text_argument = resolve_typing(argument)
                self._text_arguments.append(text_argument)

    def _build_routing_regex(self) -> None:
        """
        Выстраивает регулярное выражение, по которому
        определяется вызов команды. Не включает в себя
        аргументы, т.к. для них задается своя логика фильтром
        """
        # Экранирование специальных символов, если такое указано
        if self._allow_regexes:
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

        self._routing_regex = re.compile(
            prefixes_regex + names_regex,
            flags=self._routing_re_flags,
        )
