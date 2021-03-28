from __future__ import annotations

import abc
import typing as ty


class Event(abc.ABC):
    """ """
    def __init__(self, content: ty.Union[dict, list]):
        self._content = content

    @property
    def content(self) -> ty.Union[dict, list]:
        """
        Сырой объект события (то, что пришло в `updates`)
        """
        return self._content

    @property
    @abc.abstractmethod
    def object(self) -> ty.Union[dict, list]:
        """ """
        ...

    @property
    @abc.abstractmethod
    def type(self) -> ty.Union[int, str]:
        """ """
        ...

    def __repr__(self) -> str:
        return f"<vkquick.{self.__class__.__name__} type={self.type!r}>"
