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
from vkquick.ext.chatbot.storages import NewMessage
from vkquick.ext.chatbot.exceptions import FilterFailedError


Handler = ty.TypeVar("Handler", bound=ty.Callable[..., ty.Awaitable])


@dataclasses.dataclass
class Command(ty.Generic[Handler]):

    handler: Handler
    prefixes: ty.Optional[ty.Optional[ty.Set[str]]] = None
    names: ty.Optional[ty.Set[str]] = None
    enable_regexes: bool = False
    routing_re_flags: re.RegexFlag = re.IGNORECASE
    filter: ty.Optional[Filter] = None

    def __post_init__(self):
        self._routing_regex: ty.Pattern
        self._build_routing_regex()

        self._text_arguments: ty.List[CommandTextArgument] = []
        self._message_storage_argument_name = None
        self._message_storage_argument_name: str
        self._parse_handler_arguments()

    def update_prefix(self, *prefixes: str) -> None:
        if not self.prefixes:
            self.prefixes = set(prefixes)
            self._build_routing_regex()

    async def handle_message(self, message_storage: NewMessage) -> None:
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

    async def _run_through_filters(self, message_storage: NewMessage) -> bool:
        if self.filter is not None:
            try:
                await self.filter.make_decision(message_storage)
            except FilterFailedError:
                return False
            else:
                return True
        return True

    async def _make_arguments(
        self, message_storage: NewMessage, arguments_string: str
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
        if self._message_storage_argument_name is not None:
            arguments[self._message_storage_argument_name] = message_storage
        return arguments

    async def _call_handler(self, message_storage, arguments) -> None:
        handler_response = await self.handler(**arguments)
        if handler_response is not None:
            await message_storage.mp.reply(handler_response)

    def _parse_handler_arguments(self) -> None:
        parameters = inspect.signature(self.handler).parameters
        for name, argument in parameters.items():
            if argument.annotation is NewMessage:
                self._message_storage_argument_name = argument.name
                if self._text_arguments:
                    warnings.warn(
                        "Set `NewMessage` argument the first "
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
        if self.enable_regexes:
            names = self.names
            prefixes = self.prefixes
        else:
            names = {re.escape(name) for name in self.names}
            prefixes = {re.escape(prefix) for prefix in self.prefixes}

        names_regex = "|".join(names)
        prefixes_regex = "|".join(prefixes)

        if len(self.names) > 1:
            names_regex = f"(?:{names_regex})"

        if len(self.prefixes) > 1:
            prefixes_regex = f"(?:{prefixes_regex})"

        summary_regex = prefixes_regex + names_regex
        self._routing_regex = re.compile(
            summary_regex,
            flags=self.routing_re_flags,
        )
