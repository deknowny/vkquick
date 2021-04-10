from __future__ import annotations

import abc
import dataclasses
import typing as ty

from vkquick.ext.chatbot.command.context import Context
from vkquick.ext.chatbot.exceptions import BadArgumentError


class CommandTextArgument(ty.NamedTuple):
    argument_name: str
    cutter: TextCutter
    argument_settings: Argument


@dataclasses.dataclass
class Argument:
    description: ty.Optional[str] = None
    cast_to_type: bool = True
    callbacks: ty.List[
        ty.Callable[[Context], ty.Awaitable[ty.Any]]
    ] = dataclasses.field(default_factory=list)
    cutter: ty.Optional[TextCutter] = None
    default: ty.Optional = None
    default_factory: ty.Optional[ty.Callable[[], ty.Any]] = None


@dataclasses.dataclass
class CutterParsingResponse:
    parsed_part: ty.Any
    new_arguments_string: str
    extra: dict = dataclasses.field(default_factory=dict)


class TextCutter(abc.ABC):
    def __init__(self, *, typevars: ty.Optional[ty.List[TextCutter]] = None):
        self._typevars = typevars or []

    @property
    def typevars(self) -> ty.List[TextCutter]:
        return self._typevars

    @abc.abstractmethod
    async def cut_part(
        self, ctx: Context, arguments_string: str
    ) -> CutterParsingResponse:
        ...

    def __repr__(self):
        return f"{self.__class__.__name__}(generic_types={self._typevars})"


def cut_part_via_regex(
    regex: ty.Pattern,
    arguments_string: str,
    *,
    group: ty.Union[str, int] = 0,
    factory: ty.Optional[ty.Callable[[str], ty.Any]] = None,
) -> CutterParsingResponse:
    matched = regex.match(arguments_string)
    if matched:
        new_arguments_string = arguments_string[matched.end() :]
        parsed_part = matched.group(group)
        if factory is not None:
            parsed_part = factory(parsed_part)
        return CutterParsingResponse(
            parsed_part, new_arguments_string, extra={"match_object": matched}
        )

    raise BadArgumentError("Regex didn't matched")
