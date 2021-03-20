import enum
import typing as ty

from vkquick.bases.filter import Filter
from vkquick.exceptions import FilterFailedError


@enum.unique
class EventHandlingStatus(enum.Enum):
    INCORRECT_EVENT_TYPE = enum.auto()
    FILTER_FAILED = enum.auto()
    INCORRECT_PREPARED_ARGUMENTS = enum.auto()
    ERROR_RAISED_BY_HANDLER_CALL = enum.auto()
    ERROR_RAISED_BY_POST_HANDLING_CALLBACK = enum.auto()
    CALLED_HANDLER_SUCCESSFULLY = enum.auto()

    UNEXPECTED_ERROR_OCCURRED = enum.auto()


class StatusPayload:
    ...


class IncorrectEventType(StatusPayload, ty.NamedTuple):
    ...


class IncorrectPreparedArguments(StatusPayload, ty.NamedTuple):
    raised_error: TypeError


class ErrorRaisedByPostHandlingCallback(StatusPayload, ty.NamedTuple):
    raised_error: Exception


class CalledHandlerSuccessfully(StatusPayload, ty.NamedTuple):
    handler_returned_value: ty.Any


class ErrorRaisedByHandlerCall(StatusPayload, ty.NamedTuple):
    raised_error: Exception


class FilterFailed(StatusPayload, ty.NamedTuple):
    filter: Filter
    raised_error: FilterFailedError


class UnexpectedErrorOccurred(StatusPayload, ty.NamedTuple):
    raised_error: Exception
