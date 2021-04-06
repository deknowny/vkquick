from __future__ import annotations

import enum
import typing as ty


from vkquick.event_handler.statuses import StatusPayload

if ty.TYPE_CHECKING:
    from vkquick.ext.chatbot.exceptions import BadArgumentError
    from vkquick.ext.chatbot.filters.command.command import CommandTextArgument


@enum.unique
class CommandStatus(enum.Enum):
    """Возможные статусы обработки"""

    NOT_ROUTED = enum.auto()

    INCORRECT_ARGUMENT = enum.auto()

    UNEXPECTED_ARGUMENT = enum.auto()

    MISSED_ARGUMENT = enum.auto()


class NotRouted(StatusPayload, ty.NamedTuple):
    ...


class IncorrectArgument(StatusPayload, ty.NamedTuple):
    command_argument: CommandTextArgument
    remain_string: str
    parsing_error: BadArgumentError


class UnexpectedArgument(StatusPayload, ty.NamedTuple):
    remain_string: str


class MissedArgument(StatusPayload, ty.NamedTuple):
    remain_string: str
    command_argument: CommandTextArgument
