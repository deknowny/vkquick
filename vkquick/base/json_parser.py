from __future__ import annotations

import abc
import typing as ty


class JSONParser(abc.ABC):
    """
    Интерфейс сериализации/десериализации JSON
    """

    @staticmethod
    @abc.abstractmethod
    def dumps(data: ty.Dict[str, ty.Any]) -> ty.Union[str, bytes]:
        """
        Сериалиация объекта `data`
        """

    @staticmethod
    @abc.abstractmethod
    def loads(string: ty.Union[str, bytes]) -> ty.Dict[str, ty.Any]:
        """
        Десериализует JSON из `string`
        """
