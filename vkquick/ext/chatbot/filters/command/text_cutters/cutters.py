import re
import typing as ty

from vkquick.ext.chatbot.exceptions import BadArgumentError
from vkquick.ext.chatbot.filters.command.context import CommandContext
from vkquick.ext.chatbot.filters.command.text_cutters.base import (
    TextCutter, CutterParsingResponse, cut_part_via_regex
)


class IntegerCutter(TextCutter):

    _pattern = re.compile(r"([+|-]?\d+)")

    def cut_part(self, arguments_string: str) -> CutterParsingResponse:
        return cut_part_via_regex(self._pattern, arguments_string)

    async def cast_to_type(self, ctx: CommandContext, parsing_response: CutterParsingResponse) -> int:
        return int(parsing_response.parsed_part)


class FloatCutter(TextCutter):

    _pattern = re.compile(r"([+|-]?\d*(?:\.\d+))")

    def cut_part(self, arguments_string: str) -> CutterParsingResponse:
        return cut_part_via_regex(self._pattern, arguments_string)

    async def cast_to_type(self, ctx: CommandContext, parsing_response: CutterParsingResponse) -> float:
        return float(parsing_response.parsed_part)


class WordCutter(TextCutter):

    _pattern = re.compile(r"(\S+)")

    def cut_part(self, arguments_string: str) -> CutterParsingResponse:
        return cut_part_via_regex(self._pattern, arguments_string)

    async def cast_to_type(self, ctx: CommandContext, parsing_response: CutterParsingResponse) -> str:
        return parsing_response.parsed_part


class StringCutter(TextCutter):

    _pattern: re.Pattern

    def __init__(self, dotall: bool = True, **kwargs):
        if dotall:
            flags = re.DOTALL
        else:
            flags = 0
        self._pattern = re.compile(r"(.+)", flags=flags)
        TextCutter.__init__(self, **kwargs)

    def cut_part(self, arguments_string: str) -> CutterParsingResponse:
        return cut_part_via_regex(self._pattern, arguments_string)

    async def cast_to_type(self, ctx: CommandContext, parsing_response: CutterParsingResponse) -> str:
        return parsing_response.parsed_part


class OptionalCutter(TextCutter):

    def __init__(
        self, *, default: ty.Optional = None,
        default_factory: ty.Optional[ty.Callable[[], ty.Any]] = None,
        **kwargs
    ) -> None:
        self._default = default
        self._default_factory = default_factory
        TextCutter.__init__(self, **kwargs)

    def cut_part(self, arguments_string: str) -> CutterParsingResponse:
        try:
            parsing_response = self._generic_types[0].cut_part(arguments_string)
        except BadArgumentError:
            return CutterParsingResponse(
                "", arguments_string, extra={"optional": True}
            )
        else:
            parsing_response.extra["optional"] = False
            return parsing_response

    async def cast_to_type(
        self, ctx: CommandContext, parsing_response: CutterParsingResponse
    ) -> ty.Any:
        if parsing_response.extra["optional"]:
            if self._default_factory is not None:
                return self._default_factory()
            else:
                # `None` или установленное значение
                return self._default
        else:
            return await self._generic_types[0].cast_to_type(ctx, parsing_response)
