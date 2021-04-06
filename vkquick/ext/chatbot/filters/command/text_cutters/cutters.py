import re
import typing as ty

from vkquick.ext.chatbot.filters.command.context import CommandContext
from vkquick.ext.chatbot.filters.command.text_cutters.base import (
    TextCutter,
    CutterParsingResponse,
    cut_part_via_regex,
)


class Integer(TextCutter):

    _pattern = re.compile(r"(\d+)")

    def cut_part(self, arguments_string: str) -> CutterParsingResponse:
        return cut_part_via_regex(self._pattern, arguments_string)

    def cast_to_type(self, ctx: CommandContext, parsed_part: str) -> ty.Any:
        return int(parsed_part)
