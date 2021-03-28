from __future__ import annotations

import abc
import typing as ty


class JSONParser(abc.ABC):
    """Неймспейс, объединяющий методы сериализации и десериализации
    JSON в один протокол. Имплементации используются для
    декодирования/кодированния JSON ответов от вк.
    Имплементации некоторых из JSON-библиотек можно
    найти в `vkquick/json_parsers.py`

    Args:

    Returns:

    """

    @staticmethod
    @abc.abstractmethod
    def dumps(data: ty.Dict[str, ty.Any]) -> ty.Union[str, bytes]:
        """Метод, сериализующий JSON в строку

        Args:
          data: Сериализуемое значение (передаются только словари)
          data: ty.Dict[str:
          ty.Any]: 
          data: ty.Dict[str: 

        Returns:
          : JSON-строку

        """

    @staticmethod
    @abc.abstractmethod
    def loads(string: ty.Union[str, bytes]) -> ty.Dict[str, ty.Any]:
        """Метод, сериализующий JSON в строку

        Args:
          string: JSON-строка
          string: ty.Union[str:
          bytes]: 
          string: ty.Union[str: 

        Returns:
          : Словарь, который был объектом в строке

        """
