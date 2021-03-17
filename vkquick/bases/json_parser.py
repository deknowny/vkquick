from __future__ import annotations

import abc
import typing as ty


class JSONParser(abc.ABC):
    """
    Неймспейс, объединяющий методы сериализации и десериализации
    JSON в один протокол. Имплементации используются для
    декодирования/кодированния JSON ответов от вк.
    Имплементации некоторых из JSON-библиотек можно
    найти в `vkquick/json_parsers.py`
    """

    @staticmethod
    @abc.abstractmethod
    def dumps(data: ty.Dict[str, ty.Any]) -> ty.Union[str, bytes]:
        """
        Метод, сериализующий JSON в строку

        :param data: Сериализуемое значение (передаются только словари)
        :return: JSON-строку
        """

    @staticmethod
    @abc.abstractmethod
    def loads(string: ty.Union[str, bytes]) -> ty.Dict[str, ty.Any]:
        """
        Метод, сериализующий JSON в строку

        :param string: JSON-строка
        :return: Словарь, который был объектом в строке
        """
