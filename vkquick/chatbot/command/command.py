from __future__ import annotations

import dataclasses
import inspect
import re
import typing
import warnings

from loguru import logger

from vkquick.chatbot.base.cutter import (
    CommandTextArgument,
    InvalidArgumentConfig,
)
from vkquick.chatbot.base.filter import BaseFilter
from vkquick.chatbot.base.handler_container import HandlerMixin
from vkquick.chatbot.command.adapters import resolve_typing
from vkquick.chatbot.exceptions import BadArgumentError, FilterFailedError
from vkquick.chatbot.storages import NewMessage

Handler = typing.TypeVar(
    "Handler", bound=typing.Callable[..., typing.Awaitable]
)


@dataclasses.dataclass
class Command(HandlerMixin):
    prefixes: typing.List[str] = dataclasses.field(default_factory=list)
    names: typing.List[str] = dataclasses.field(default_factory=list)
    routing_re_flags: re.RegexFlag = re.IGNORECASE
    filter: typing.Optional[BaseFilter] = None
    description: typing.Optional[str] = None
    exclude_from_autodoc: bool = False
    invalid_argument_config: InvalidArgumentConfig = dataclasses.field(
        default_factory=InvalidArgumentConfig
    )

    def __post_init__(self):
        self.prefixes = list(self.prefixes)
        self.names = list(self.names)
        if not self.names:
            self.names = self.handler.__name__
        self.handler = logger.catch(self.handler)

        self._text_arguments: typing.List[CommandTextArgument] = []
        self._message_storage_argument_name = None
        self._message_storage_argument_name: str
        self._parse_handler_arguments()

        self._routing_regex: typing.Pattern
        self._build_routing_regex()

    @property
    def trusted_description(self) -> str:
        if self.description is None:
            docstring = inspect.getdoc(self.handler)
            if docstring is None:
                return "Описание отсутствует"
            return docstring
        return self.description

    @property
    def text_arguments(self) -> typing.List[CommandTextArgument]:
        return self._text_arguments

    def update_prefix(self, *prefixes: str) -> None:
        if not self.prefixes:
            self.prefixes = list(set(prefixes))
            self._build_routing_regex()

    async def handle_message(self, message_storage: NewMessage) -> None:
        is_routing_matched = self._routing_regex.match(
            message_storage.msg.text
        )
        if is_routing_matched:
            arguments = await self._make_arguments(
                message_storage,
                message_storage.msg.text[is_routing_matched.end() :],
            )
            if arguments is not None:
                passed_filter = await self._run_through_filters(
                    message_storage
                )
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
    ) -> typing.Optional[typing.Dict[str, typing.Any]]:
        arguments = {}
        remain_string = arguments_string.lstrip()
        # argtype is None после обработки, если у команды не было аргументов вовсе
        argtype = None
        for argtype in self._text_arguments:
            remain_string = remain_string.lstrip()
            try:
                parsing_response = await argtype.cutter.cut_part(
                    message_storage, remain_string
                )
            except BadArgumentError as err:
                if self.invalid_argument_config is not None:
                    await self.invalid_argument_config.on_invalid_argument(
                        remain_string=remain_string,
                        ctx=message_storage,
                        argument=argtype,
                    )
                return None
            else:
                remain_string = parsing_response.new_arguments_string.lstrip()
                arguments[
                    argtype.argument_name
                ] = parsing_response.parsed_part

        if remain_string:
            if argtype is not None:
                await self.invalid_argument_config.on_invalid_argument(
                    remain_string=remain_string,
                    ctx=message_storage,
                    argument=argtype,
                )
            return None
        if self._message_storage_argument_name is not None:
            arguments[self._message_storage_argument_name] = message_storage
        return arguments

    async def _call_handler(
        self, message_storage: NewMessage, arguments: dict
    ) -> None:
        logger.opt(colors=True).success(
            "Call command <m>{com_name}</m><w>({args})</w>".format(
                com_name=self.handler.__name__,
                args=", ".join(
                    f"<c>{key}</c>=<y>{value!r}</y>"
                    for key, value in arguments.items()
                ),
            )
        )
        handler_response = await self.handler(**arguments)
        if handler_response is not None:
            await message_storage.reply(handler_response)

    def _parse_handler_arguments(self) -> None:
        parameters = inspect.signature(self.handler).parameters
        for name, argument in parameters.items():
            if typing.get_origin(argument.annotation) == NewMessage:
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
        # Экранирование специальных символов
        names = {re.escape(name) for name in self.names}
        prefixes = {re.escape(prefix) for prefix in self.prefixes}

        names_regex = "|".join(names)
        prefixes_regex = "|".join(prefixes)

        if len(self.names) > 1:
            names_regex = f"(?:{names_regex})"

        if len(self.prefixes) > 1:
            prefixes_regex = f"(?:{prefixes_regex})"

        summary_regex = prefixes_regex + names_regex

        # Если у команды есть аргументы,
        # то при ее вызове после имени команды должны идти пробельные символы
        # или аргументов не должно быть вовсе
        if self._text_arguments:
            summary_regex += r"(?:$|\s+)"

        self._routing_regex = re.compile(
            summary_regex,
            flags=self.routing_re_flags,
        )
