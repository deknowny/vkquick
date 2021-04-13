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


@dataclasses.dataclass
class StopEventProcessing(Exception):
    """
    Используется мидлварами в `foreword` методе, чтобы
    остановить обработку события. Если это исключение
    поднято, ни один из обработчиков событий не вызовется,
    но при этом `afterword` методы вызовутся
    """
    reason: ty.Optional[str] = None
    extra: dict = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class StopHandlingEvent(Exception):
    """
    Поднимается внутри обработчика события,
    чтобы остановить процесс обработки события.
    Может быть поднято как и при успешной обработке,
    так и неуспешной

    Arguments:
        status: Статус обработки события. Например, один
            из фильтров не прошел обработку или событие
            не подходит по своему типу
        payload: Поле с дополнительной информацией
            о статусе обработки
    """
    status: EventHandlingStatus
    payload: StatusPayload


@dataclasses.dataclass
class ExpectedMiddlewareToBeUsed(Exception):
    """
    Исключение поднимается, если какая-либо логика
    требует наличие специального мидллвара в боте

    Arguments:
        middleware_name: Имя мидлвара, который необходимо добавить
    """
    middleware_name: str

    def __str__(self):
        return (
            f"Expected `{self.middleware_name}` middleware to be used."
            "Add it to the bot instance"
        )


@dataclasses.dataclass
class NotCompatibleFilterError(Exception):
    """
    Поднимается, если используемый фильтр
    не способен обработать событие, которое
    может обработать обработчик событий

    Args:
        filter: Объект фильтра,
            который не может обработать одно из обрабатываемых
            событий обработчика событий, куда он прикреплен
        event_handler: Объект обработчика событий, куда был прикреплен фильтр
        uncovered_event_types: События, которые не может покрыть фильтр
    """

    filter: Filter
    event_handler: EventHandler
    uncovered_event_types: ty.Set[ty.Union[int, str]]

    def __str__(self) -> str:
        return (
            f"Filter `{self.filter.__class__.__name__}` "
            f"can't handle event types "
            f"`{self.uncovered_event_types}` "
            f"that can be handled by `{self.event_handler}`"
        )


@dataclasses.dataclass
class FilterFailedError(Exception):
    """
    Вызывается внутри фильтров, если полученное им
    события не подходит по каким-либо критериям

    Arguments:
        reason: Причина, по которой фильтр не прошел обработку
        extra: Дополнительные параметры (информация), которую
            может сообщить фильтр о причине отмены обработки
    """

    reason: ty.Optional[str] = None
    extra: dict = dataclasses.field(default_factory=dict)


class _ParamsScheme(tye.TypedDict):
    """
    Структура параметров, возвращаемых
    при некорректном обращении к API
    """

    key: str
    value: str  # Даже если в запросе было передано число, значение будет строкой


@dataclasses.dataclass
class VKAPIError(Exception):
    """
    Исключение, поднимаемое при некорректном вызове API запроса.
    Инициализируется через метод класса `destruct_response`
    для деструктуризации ответа от вк

    Args:
        pretty_exception_text: Красиво выстроенное сообщение с ошибкой от API
        description: Описание ошибки (из API ответа)
        status_code: Статус-код ошибки (из API ответа)
        request_params: Параметры запроса, в ответ на который пришла ошибка
        extra_fields: Дополнительные поля (из API ответа)
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

        Arguments:
            response: Ответ с ошибкой, полученный от API
        Returns:
            Новый объект исключения
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

    def __str__(self) -> str:
        return self.pretty_exception_text
