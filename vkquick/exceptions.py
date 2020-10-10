"""
Дополнительные исключения
"""
from __future__ import annotations
import dataclasses
import typing as ty

import click


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
        status_code, description, request_params = response["error"].values()

        pretty_exception_text = (
            click.style(f"\n[{status_code}] ", fg="red")
            + click.style(f"{description}\n\n", fg="red", bold=True)
            + click.style("Request params:", bold=True)
        )

        for pair in request_params:
            key = click.style(pair["key"], fg="yellow")
            value = click.style(pair["value"], fg="cyan")
            pretty_exception_text += f"\n{key} = {value}"

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
