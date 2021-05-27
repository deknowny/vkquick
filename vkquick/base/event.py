from __future__ import annotations

import abc
import typing

EventType = typing.Union[str, int]


class BaseEvent(abc.ABC):
    """ """

    def __init__(self, content: typing.Union[dict, list]):
        self._content = content

    @property
    def content(self) -> typing.Union[dict, list]:
        """
        Сырой объект события (то, что пришло в `updates`)
        """
        return self._content

    @property
    @abc.abstractmethod
    def object(self) -> typing.Union[dict, list]:
        """ """
        ...

    @property
    @abc.abstractmethod
    def type(self) -> EventType:
        """ """
        ...

    def __repr__(self) -> str:
        return f"<vkquick.{self.__class__.__name__} type={self.type!r}>"
