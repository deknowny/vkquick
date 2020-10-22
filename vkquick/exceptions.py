"""
Дополнительные исключения
"""
from __future__ import annotations
import dataclasses
import typing as ty

import sty


class _ParamsScheme(ty.TypedDict):
    """
    Струкутра параметров, возвращаемых
    при некорректном обращении к API
    """

    key: str
    value: str  # Даже если в запрсосе было передано число, значение будет строкой


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

    @classmethod
    def destruct_response(cls, response: ty.Dict[str, ty.Any]) -> VkApiError:
        """
        Разбирает ответ от вк про некорректный API запрос
        на части и инициализирует сам объект исключения
        """
        status_code = response["error"].pop("error_code")
        description = response["error"].pop("error_msg")
        request_params = response["error"].pop("request_params")

        pretty_exception_text = (
            sty.fg.red
            + f"\n[{status_code}] "
            + sty.fg.rs
            + f"{description}\n\n"
            + sty.fg.li_white
            + "Request params:"
            + sty.fg.rs
        )

        for pair in request_params:
            key = sty.fg.yellow + pair["key"] + sty.fg.rs
            value = sty.fg.cyan + pair["value"] + sty.fg.rs
            pretty_exception_text += f"\n{key} = {value}"

        # Если остались дополнительные поля
        if response["error"]:
            pretty_exception_text += (
                "\n\nThere are some extra fields:\n"
                f"{response['error']}"
            )

        return cls(
            pretty_exception_text=pretty_exception_text,
            description=description,
            status_code=status_code,
            request_params=request_params,
        )

    def __str__(self):
        return self.pretty_exception_text


class BotReloadNow(Exception):
    """
    Поднимается, когда требуется остановить работу бота
    """
