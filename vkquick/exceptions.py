"""
Дополнительные исключения
"""
from __future__ import annotations
import dataclasses
import typing as ty

import huepy


class _ParamsScheme(ty.TypedDict):
    """
    Структура параметров, возвращаемых
    при некорректном обращении к API
    """

    key: str
    value: str  # Даже если в запросе было передано число, значение будет строкой


@dataclasses.dataclass
class VkApiError(Exception):
    """
    Исключение, поднимаемое при некорректном вызове API запроса.
    Инициализируется через метод класса `destruct_response`
    для деструктуризации ответа от вк
    """

    pretty_exception_text: str
    description: str
    status_code: int
    request_params: _ParamsScheme
    extra_fileds: dict

    @classmethod
    def destruct_response(cls, response: ty.Dict[str, ty.Any]) -> VkApiError:
        """
        Разбирает ответ от вк про некорректный API запрос
        на части и инициализирует сам объект исключения
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
            extra_fileds=response["error"],
        )

    def __str__(self):
        return self.pretty_exception_text
