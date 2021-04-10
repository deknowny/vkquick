import enum
import typing as ty

from vkquick.bases.filter import Filter
from vkquick.exceptions import FilterFailedError


@enum.unique
class EventHandlingStatus(enum.Enum):
    """Возможные статусы обработки"""

    INCORRECT_EVENT_TYPE = enum.auto()
    """
    Тип события не обрабатывается этим хэндлером
    """

    FILTER_FAILED = enum.auto()
    """
    Один из фильтров не прошел обработку
    """

    CALLED_HANDLER_SUCCESSFULLY = enum.auto()
    """
    Вызов хэндлера прошел успешно
    """

    UNEXPECTED_ERROR_OCCURRED = enum.auto()


class StatusPayload:
    """ "Контейнер" с дополнительной информацией на
    каждый статус обработки

    Args:

    Returns:

    """


class IncorrectEventType(StatusPayload, ty.NamedTuple):
    """Контейнер для `INCORRECT_EVENT_TYPE` статуса"""


class FilterFailed(StatusPayload, ty.NamedTuple):
    """Контейнер для `FILTER_FAILED` статуса"""

    filter: Filter
    """
    Объект фильтра, который не прошел обработку
    """

    raised_error: FilterFailedError
    """
    Поднятое фильтром исключение (исключение может
    хранить в себе дополнительные полезные поля)
    """


class CalledHandlerSuccessfully(StatusPayload, ty.NamedTuple):
    """Контейнер для `CALLED_HANDLER_SUCCESSFULLY` статуса"""

    handler_returned_value: ty.Any
    """
    Значение, которое вернул обработчик
    """


class UnexpectedErrorOccurred(StatusPayload, ty.NamedTuple):
    """Поднято неожидаемое исключение. Причиной может быть как
    пользовательский код, так и код vkquick

    Args:

    Returns:

    """

    raised_error: Exception
    """
    Объект исключения
    """
