"""
Дополнительные исключения
"""
from __future__ import annotations

import dataclasses
import typing as ty

import huepy
import typing_extensions as tye

exceptions_storage: ty.Dict[int, ty.Type[APIError]] = {}


class _ParamsScheme(tye.TypedDict):
    """
    Структура параметров, возвращаемых
    при некорректном обращении к API
    """

    key: str
    value: str  # Даже если в запросе было передано число, значение будет строкой


@dataclasses.dataclass
class APIError(Exception):
    """
    Исключение, поднимаемое при некорректном вызове API запроса.

    Arguments:
        pretty_exception_text: Красиво выстроенное сообщение с ошибкой от API
        description: Описание ошибки (из API ответа)
        status_code: Статус-код ошибки (из API ответа)
        request_params: Параметры запроса, в ответ на который пришла ошибка
        extra_fields: Дополнительные поля (из API ответа)
    """

    description: str
    status_code: int
    request_params: ty.List[_ParamsScheme]
    extra_fields: dict

    def __class_getitem__(
        cls, code: ty.Union[int, ty.Tuple[int, ...]]
    ) -> ty.Tuple[ty.Type[APIError]]:
        result_classes = []
        codes = (code,) if isinstance(code, int) else code
        for code in codes:
            if code in exceptions_storage:
                result_classes.append(exceptions_storage[code])
            else:
                new_class = type(f"APIError{code}", (APIError,), {})
                exceptions_storage[code] = new_class
                result_classes.append(new_class)

        return tuple(result_classes)

    @classmethod
    def destruct_response(cls, response: ty.Dict[str, ty.Any]) -> APIError:
        """Разбирает ответ от вк про некорректный API запрос
        на части и инициализирует сам объект исключения

        Arguments:
            response: Ответ с ошибкой, полученный от API
        Returns:
            Новый объект исключения
        """

    def __str__(self) -> str:
        pretty_exception_text = (
            huepy.red(f"\n[{self.status_code}]")
            + f" {self.description}\n\n"
            + huepy.grey("Request params:")
        )

        for param in self.request_params:
            key = param["key"]
            value = param["value"]
            key = huepy.yellow(key)
            value = huepy.cyan(value)
            pretty_exception_text += f"\n{key} = {value}"

        # Если остались дополнительные поля
        if self.extra_fields:
            pretty_exception_text += (
                "\n\n"
                + huepy.info("There are some extra fields:\n")
                + str(self.extra_fields)
            )
        return pretty_exception_text
