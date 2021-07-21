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

    _html_to_message = False

    @abc.abstractmethod
    async def cut_part(
        self, ctx: NewMessage, arguments_string: str
    ) -> CutterParsingResponse:
        ...

    @abc.abstractmethod
    def gen_doc(self) -> str:
        ...

    def gen_message_doc(self) -> str:
        message = self.gen_doc()
        if self._html_to_message:
            message = html_list_to_message(message)
        return message


def cut_part_via_regex(
    regex: typing.Pattern,
    arguments_string: str,
    *,
    group: typing.Union[str, int] = 0,
    factory: typing.Optional[typing.Callable[[str], T]] = None,
    error_description: typing.Optional[str] = None,
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
    prefix_sign: str = "💡"
    invalid_argument_template: str = (
        "{prefix_sign} Некорректное значение "
        "`{incorrect_value}`. Необходимо передать {cutter_description}"
    )
    laked_argument_template: str = (
        "{prefix_sign} Необходимо передать {cutter_description}"
    )
    prefix_sign_used: bool = True
    incorrect_value_used: bool = True
    cutter_description_used: bool = True

    async def on_invalid_argument(
        self,
        *,
        remain_string: str,
        ctx: NewMessage,
        argument: CommandTextArgument,
    ):
        # TODO: mentions

        prefix_sign = self.prefix_sign if self.prefix_sign_used else ""
        cutter_description = (
            (
                argument.argument_settings.description
                or argument.cutter.gen_message_doc()
            )
            if self.cutter_description_used
            else ""
        )

        if remain_string:
            incorrect_value = remain_string.split(maxsplit=1)[0]
            incorrect_value = (
                incorrect_value if self.incorrect_value_used else ""
            )
            tip_response = self.invalid_argument_template.format(
                prefix_sign=prefix_sign,
                incorrect_value=incorrect_value,
                cutter_description=cutter_description,
            )

        else:
            tip_response = self.laked_argument_template.format(
                prefix_sign=prefix_sign,
                cutter_description=cutter_description,
            )

        await ctx.reply(tip_response)


def html_list_to_message(view: str) -> str:
    return (
        view.replace("<br>", "\n")
        .replace("</ol>", "")
        .replace("<ol><li>", "\n— ")
        .replace("</li>\n<li>", "\n— ")
        .replace("</li>", "")
        .replace("<code>", "`")
        .replace("</code>", "`")
    )
