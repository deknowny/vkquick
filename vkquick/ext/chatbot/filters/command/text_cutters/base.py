import abc
import typing as ty

from vkquick.event_handler.context import EventHandlingContext
from vkquick.ext.chatbot.exceptions import BadArgumentError


class CutterParsingResponse(ty.NamedTuple):
    parsed_part: str
    new_arguments_string: str


def cut_part_via_regex(
    regex: ty.Pattern,
    arguments_string: str,
) -> ty.Tuple[ty.Match, str]:
    matched = regex.match(arguments_string)
    if matched:
        new_arguments_string = arguments_string[
            matched.end() :
        ]  # black: ignore
        return CutterParsingResponse(
            matched.lastgroup(), new_arguments_string
        )

    raise BadArgumentError("Regex didn't matched")


class TextCutter(abc.ABC):
    @abc.abstractmethod
    def cut_part(self, arguments_string: str) -> CutterParsingResponse:
        ...

    @abc.abstractmethod
    async def convert_to_type(
        self, ehctx: EventHandlingContext, parsed_part: str
    ) -> ty.Any:
        ...
