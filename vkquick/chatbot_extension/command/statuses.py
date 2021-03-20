from __future__ import annotations

import typing as ty
import enum

from vkquick.chatbot_extension.text_cutters.base import TextCutter


@enum.unique
class CommandValidatingStatus(enum.Enum):

    ROUTING_UNMATCHED = enum.auto()
    EXCESS_ARGUMENT = enum.auto()
    DISADVANTAGED_ARGUMENT = enum.auto()
    INCORRECT_ARGUMENT = enum.auto()
    ARGUMENT_CALLBACK_FAILED = enum.auto()
    PASSED = enum.auto()


class _StatusPayload:
    ...


class RoutingUnmatched(_StatusPayload, ty.NamedTuple):
    ...


class ExcessArgument(_StatusPayload, ty.NamedTuple):
    remaining_string: str


class DisadvantagedArgument(_StatusPayload, ty.NamedTuple):
    name: str
    cutter: TextCutter


class IncorrectArgument(_StatusPayload, ty.NamedTuple):
    unparsed_string: str
    name: str
    cutter: TextCutter


class ArgumentCallbackFailed(_StatusPayload, ty.NamedTuple):
    name: str
    cutter: TextCutter
    callback_func: ty.Callable


class Passed(_StatusPayload, ty.NamedTuple):
    ...




