from __future__ import annotations

import abc
import re
import typing as ty

from vkquick.ext.chatbot.filters.command.context import CommandContext
from vkquick.ext.chatbot.exceptions import BadArgumentError


class CommandTextArgument(ty.NamedTuple):
    argument_name: str
    cutter: TextCutter
    argument_settings: Argument


class Argument:
    def __init__(
        self,
        *,
        description: ty.Optional[str] = None,
        cast_to_type: bool = True,
        callbacks: ty.Optional[
            ty.List[ty.Callable[[CommandContext], ty.Awaitable[ty.Any]]]
        ] = None
    ) -> None:
        self._description = description
        self._cast_to_type = cast_to_type
        self._callbacks = callbacks
        self._extra = {}

    def add_extra(self, **kwargs):
        self._extra = kwargs

    @property
    def description(self) -> str:
        return self._description

    @property
    def cast_to_type(self) -> bool:
        return self._cast_to_type

    @property
    def callbacks(
        self,
    ) -> ty.List[ty.Callable[[CommandContext], ty.Awaitable[ty.Any]]]:
        return self._callbacks

    @property
    def extra(self) -> dict:
        return self._extra


class CutterParsingResponse(ty.NamedTuple):
    parsed_part: str
    new_arguments_string: str


class TextCutter(abc.ABC):
    def __init__(self, *, generic_types: ty.Optional[ty.List[type]] = None):
        self._generic_types = generic_types or []

    @property
    def generic_types(self) -> ty.List[type]:
        return self._generic_types

    @abc.abstractmethod
    def cut_part(self, arguments_string: str) -> CutterParsingResponse:
        ...

    @abc.abstractmethod
    async def cast_to_type(
        self, ctx: CommandContext, parsed_part: str
    ) -> ty.Any:
        ...


def cut_part_via_regex(
    regex: ty.Pattern, arguments_string: str, group: ty.Union[str, int] = 0
) -> CutterParsingResponse:
    matched = regex.match(arguments_string)
    if matched:
        new_arguments_string = arguments_string[
            matched.end() :
        ]
        return CutterParsingResponse(
            matched.group(group), new_arguments_string
        )

    raise BadArgumentError("Regex didn't matched")
