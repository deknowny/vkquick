from __future__ import annotations

import abc
import typing as ty


class Event(abc.ABC):

    def __init__(self, content: ty.Union[dict, list]):
        self._content = content

    @property
    def content(self) -> ty.Union[dict, list]:
        return self._content

    @property
    @abc.abstractmethod
    def type(self) -> ty.Union[int, str]:
        ...


