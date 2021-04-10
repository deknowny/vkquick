import re
import typing as ty

from vkquick.ext.chatbot.exceptions import BadArgumentError
from vkquick.ext.chatbot.filters.command.context import Context
from vkquick.ext.chatbot.filters.command.text_cutters.base import (
    TextCutter,
    CutterParsingResponse,
    cut_part_via_regex,
)


class IntegerCutter(TextCutter):

    _pattern = re.compile(r"([+|-]?\d+)")

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        return cut_part_via_regex(
            self._pattern, arguments_string, factory=int
        )


class FloatCutter(TextCutter):

    _pattern = re.compile(r"([+|-]?\d*(?:\.?\d+))")

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        return cut_part_via_regex(
            self._pattern, arguments_string, factory=float
        )


class WordCutter(TextCutter):

    _pattern = re.compile(r"(\S+)")

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        return cut_part_via_regex(self._pattern, arguments_string)


class StringCutter(TextCutter):

    _pattern = re.compile(r"(.+)", flags=re.DOTALL)

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        return cut_part_via_regex(self._pattern, arguments_string)


class ParagraphCutter(TextCutter):
    _pattern = re.compile(r"(.+)")

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        return cut_part_via_regex(self._pattern, arguments_string)


class OptionalCutter(TextCutter):
    def __init__(
        self,
        *,
        default: ty.Optional = None,
        default_factory: ty.Optional[ty.Callable[[], ty.Any]] = None,
        **kwargs
    ) -> None:
        self._default = default
        self._default_factory = default_factory
        TextCutter.__init__(self, **kwargs)

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        try:
            return await self.typevars[0].cut_part(ctx, arguments_string)
        except BadArgumentError:
            if self._default_factory is not None:
                return CutterParsingResponse(
                    parsed_part=self._default_factory(),
                    new_arguments_string=arguments_string,
                )
            else:
                # `None` или установленное значение
                return CutterParsingResponse(
                    parsed_part=self._default,
                    new_arguments_string=arguments_string,
                )
