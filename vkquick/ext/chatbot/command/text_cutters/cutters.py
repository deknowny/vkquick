import re
import typing as ty

from vkquick.ext.chatbot.command.context import Context
from vkquick.ext.chatbot.command.text_cutters.base import (
    CutterParsingResponse,
    TextCutter,
    cut_part_via_regex,
)
from vkquick.ext.chatbot.exceptions import BadArgumentError


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


class UnionCutter(TextCutter):
    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        for typevar in self.typevars:
            try:
                parsed_value = await typevar.cut_part(ctx, arguments_string)
            except BadArgumentError:
                continue
            else:
                return parsed_value

        raise BadArgumentError("Regexes didn't matched")


class GroupCutter(TextCutter):
    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        parsed_parts = []
        for typevar in self.typevars:
            try:
                parsed_value = await typevar.cut_part(ctx, arguments_string)
            except BadArgumentError as err:
                raise BadArgumentError("Regexes didn't matched") from err
            else:
                arguments_string = parsed_value.new_arguments_string
                parsed_parts.append(parsed_value.parsed_part)
                continue

        return CutterParsingResponse(
            parsed_part=tuple(parsed_parts),
            new_arguments_string=arguments_string,
        )


class _SequenceCutter(TextCutter):

    _factory: ty.Callable[[list], ty.Sequence]

    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        typevar = self.typevars[0]
        parsed_values = []
        while True:
            try:
                parsing_response = await typevar.cut_part(
                    ctx, arguments_string
                )
            except BadArgumentError:
                return CutterParsingResponse(
                    parsed_part=self._factory(parsed_values),
                    new_arguments_string=arguments_string,
                )
            else:
                arguments_string = (
                    parsing_response.new_arguments_string.lstrip()
                    .lstrip(",")
                    .lstrip()
                )
                parsed_values.append(parsing_response.parsed_part)
                continue


class MutableSequenceCutter(_SequenceCutter):

    _factory = list


class ImmutableSequenceCutter(_SequenceCutter):

    _factory = tuple


class UniqueMutableSequenceCutter(_SequenceCutter):

    _factory = set
