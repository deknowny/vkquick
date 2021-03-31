import abc
import typing as ty

from vkquick.bot import EventProcessingContext
from vkquick.ext.chatbot.exceptions import BadArgumentError


class CutterParsingResponse(ty.NamedTuple):
    matched_part: str
    new_arguments_string: str


def cut_part_via_regex(
    regex: ty.Pattern,
    arguments_string: str,
) -> ty.Tuple[ty.Match, str]:
    matched = regex.match(arguments_string)
    if matched:
        new_arguments_string = arguments_string[matched.end():]  # black: ignore
        return CutterParsingResponse(matched.lastgroup(), new_arguments_string)

    raise BadArgumentError("Regex didn't matched")


RuleCallback = ty.Callable[[EventProcessingContext, ty.Any], ty.Awaitable]


class TextCutter(abc.ABC):

    def __init__(self, *, rules: ty.Optional[ty.List[RuleCallback]] = None) -> None:
        self._rules = rules or []

    @abc.abstractmethod
    def cut_part(self, arguments_string: str) -> CutterParsingResponse:
        ...

    def add_rule(self, rule: RuleCallback) -> None:
        self._rules.append(rule)


