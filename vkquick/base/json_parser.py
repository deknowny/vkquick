from __future__ import annotations

import abc
import typing


class BaseJSONParser(abc.ABC):
    """
    Неймспейс, объединяющий методы сериализации и десериализации
    JSON в один протокол. Имплементации используются для
    декодирования/кодирования JSON ответов от вк.

    Имплементации некоторых из JSON-библиотек можно
    найти в [json_parsers.py](../json_parsers.py)
    """

    @staticmethod
    @abc.abstractmethod
    def dumps(data: typing.Dict[str, typing.Any]) -> typing.Union[str, bytes]:
        """
        Метод, сериализующий JSON в строку

        Args:
            data: Сериализуемое значение (передаются только словари)
        Returns:
            JSON-строку
        """

    @staticmethod
    @abc.abstractmethod
    def loads(
        string: typing.Union[str, bytes]
    ) -> typing.Dict[str, typing.Any]:
        """
        Метод, сериализующий JSON из строки

        Args:
            string: JSON-строка

        Returns:
            Словарь, который был объектом в строке

        """
