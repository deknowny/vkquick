"""
Дополнительные исключения
"""
from __future__ import annotations

import dataclasses
import typing as ty

import huepy
import typing_extensions as tye

if ty.TYPE_CHECKING:
    from vkquick.bases.filter import Filter
    from vkquick.event_handler.handler import EventHandler
    from vkquick.event_handler.statuses import (
        EventHandlingStatus,
        StatusPayload,
    )


class IncorrectPreparedArgumentsError(Exception):
    """ """
    def __init__(
        self,
        *,
        expected_names: ty.FrozenSet[str],
        actual_names: ty.FrozenSet[str],
    ) -> None:
        self.expected_names = expected_names
        self.actual_names = actual_names


class StopHandlingEvent(Exception):
    """ """
    def __init__(
        self, *, status: EventHandlingStatus, payload: StatusPayload
    ) -> None:
        self.status = status
        self.payload = payload


class NotCompatibleFilterError(Exception):
    """Поднимается, если используемый фильтр не способен обработать событие,
    которое может обработать обработчик событий

    Args:
      filter: Объект фильтра,
    который не может обработать одно из обрабатываемых
    событий обработчика событий, куда он прикреплен
      event_handler: Объект обработчика событий, куда был прикреплен фильтр
    :uncovered_event_types: События, которые не может покрыть фильтр. Если `Ellipsis`

    Returns:

    """

    def __init__(
        self,
        *,
        filter: Filter,
        event_handler: EventHandler,
        uncovered_event_types: ty.Set[ty.Union[int, str]],
    ):
        self.filter = filter
        self.event_handler = event_handler
        self.uncovered_event_types = uncovered_event_types

    def __str__(self):
        return (
            f"Filter `{self.filter.__class__.__name__}` "
            f"can't handle event types "
            f"`{self.uncovered_event_types}` "
            f"that can be handled by `{self.event_handler}`"
        )


class FilterFailedError(Exception):
    """ """
    def __init__(self, filter: Filter, reason: str, **extra_payload_params):
        self.filter = filter
        self.reason = reason
        self.extra = extra_payload_params

    def __str__(self):
        return (
            f"Filter `{self.filter.__class__.__name__}` "
            f"not passed because `{self.reason}`. "
            f"Extra params: `{self.extra}`"
        )


class _ParamsScheme(tye.TypedDict):
    """Структура параметров, возвращаемых
    при некорректном обращении к API

    Args:

    Returns:

    """

    key: str
    value: str  # Даже если в запросе было передано число, значение будет строкой


@dataclasses.dataclass
class VKAPIError(Exception):
    """Исключение, поднимаемое при некорректном вызове API запроса.
    Инициализируется через метод класса `destruct_response`
    для деструктуризации ответа от вк

    Args:

    Returns:

    """

    pretty_exception_text: str
    description: str
    status_code: int
    request_params: _ParamsScheme
    extra_fields: dict

    @classmethod
    def destruct_response(cls, response: ty.Dict[str, ty.Any]) -> VKAPIError:
        """Разбирает ответ от вк про некорректный API запрос
        на части и инициализирует сам объект исключения

        Args:
          response: ty.Dict[str:
          ty.Any]: 
          response: ty.Dict[str: 

        Returns:

        """
        status_code = response["error"].pop("error_code")
        description = response["error"].pop("error_msg")
        request_params = response["error"].pop("request_params")
        request_params = {
            item["key"]: item["value"] for item in request_params
        }

        pretty_exception_text = (
            huepy.red(f"\n[{status_code}]")
            + f" {description}\n\n"
            + huepy.grey("Request params:")
        )

        for key, value in request_params.items():
            key = huepy.yellow(key)
            value = huepy.cyan(value)
            pretty_exception_text += f"\n{key} = {value}"

        # Если остались дополнительные поля
        if response["error"]:
            pretty_exception_text += (
                "\n\n"
                + huepy.info("There are some extra fields:\n")
                + str(response["error"])
            )

        return cls(
            pretty_exception_text=pretty_exception_text,
            description=description,
            status_code=status_code,
            request_params=request_params,
            extra_fields=response["error"],
        )

    def __str__(self):
        return self.pretty_exception_text
