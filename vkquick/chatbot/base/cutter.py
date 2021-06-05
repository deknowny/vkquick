from __future__ import annotations

import abc
import dataclasses
import typing

from vkquick.chatbot.exceptions import BadArgumentError
from vkquick.chatbot.storages import NewMessage

T = typing.TypeVar("T")


class CommandTextArgument(typing.NamedTuple):
    argument_name: str
    cutter: Cutter
    argument_settings: Argument


@dataclasses.dataclass
class Argument:
    description: typing.Optional[str] = None
    default: typing.Optional = None
    default_factory: typing.Optional[typing.Callable[[], typing.Any]] = None
    cutter_preferences: dict = dataclasses.field(default_factory=dict)

    def setup_cutter(self, **kwargs) -> Argument:
        if self.cutter_preferences:
            raise ValueError("Cutter preferences has been already set")
        self.cutter_preferences = kwargs
        return self


@dataclasses.dataclass
class CutterParsingResponse(typing.Generic[T]):
    parsed_part: T
    new_arguments_string: str
    extra: dict = dataclasses.field(default_factory=dict)


class Cutter(abc.ABC):
    @abc.abstractmethod
    async def cut_part(
        self, ctx: NewMessage, arguments_string: str
    ) -> CutterParsingResponse:
        ...

    @abc.abstractmethod
    def gen_doc(self) -> str:
        ...

    def gen_message_doc(self) -> str:
        return self.gen_doc()


def cut_part_via_regex(
    regex: typing.Pattern,
    arguments_string: str,
    *,
    group: typing.Union[str, int] = 0,
    factory: typing.Optional[typing.Callable[[str], T]] = None,
    error_description: typing.Optional[str] = None
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

    raise BadArgumentError(error_description or "Regex didn't matched")


class InvalidArgumentConfig:
    prefix_sign = "💡"
    invalid_argument_template = (
        "{prefix_sign} Некорректное значение "
        "`{incorrect_value}`. Необходимо передать {cutter_description}"
    )

    async def on_invalid_argument(
        self,
        *,
        remain_string: str,
        ctx: NewMessage,
        argument: CommandTextArgument,
        error: BadArgumentError,
    ):
        # TODO: mentions
        incorrect_value = remain_string.split(maxsplit=1)[0]
        cutter_description = (
            argument.argument_settings.description or error.description
        )
        await ctx.reply(
            self.invalid_argument_template.format(
                prefix_sign=self.prefix_sign,
                incorrect_value=incorrect_value,
                cutter_description=cutter_description,
            )
        )

    async def on_laked_argument(
        self,
        *,
        ctx: NewMessage,
        argument: CommandTextArgument,
        error: BadArgumentError,
    ):
        ...