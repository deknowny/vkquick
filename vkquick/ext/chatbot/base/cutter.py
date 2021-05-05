from __future__ import annotations

import abc
import dataclasses
import typing as ty

from vkquick.ext.chatbot.exceptions import BadArgumentError
from vkquick.ext.chatbot.storages import NewMessage

T = ty.TypeVar("T")


class CommandTextArgument(ty.NamedTuple):
    argument_name: str
    cutter: Cutter
    argument_settings: Argument


@dataclasses.dataclass
class Argument:
    description: ty.Optional[str] = None
    callbacks: ty.List[
        ty.Callable[[NewMessage], ty.Awaitable[ty.Any]]
    ] = dataclasses.field(default_factory=list)
    default: ty.Optional = None
    default_factory: ty.Optional[ty.Callable[[], ty.Any]] = None
    cutter_preferences: dict = dataclasses.field(default_factory=dict)

    def setup_cutter(self, **kwargs) -> Argument:
        if self.cutter_preferences:
            raise ValueError("Cutter preferences has been already set")
        self.cutter_preferences = kwargs
        return self


@dataclasses.dataclass
class CutterParsingResponse(ty.Generic[T]):
    parsed_part: T
    new_arguments_string: str
    extra: dict = dataclasses.field(default_factory=dict)


class Cutter(abc.ABC):
    @abc.abstractmethod
    async def cut_part(
        self, ctx: NewMessage, arguments_string: str
    ) -> CutterParsingResponse:
        ...


def cut_part_via_regex(
    regex: ty.Pattern,
    arguments_string: str,
    *,
    group: ty.Union[str, int] = 0,
    factory: ty.Optional[ty.Callable[[str], T]] = None,
) -> CutterParsingResponse[T]:
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
