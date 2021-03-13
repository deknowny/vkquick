from __future__ import annotations

import abc
import typing as ty

from vkquick.attrdict import AttrDict


class Event(abc.ABC):

    def __init__(self, content: ty.Union[dict, list]):
        self._content = content

    @property
    def content(self):
        return self._content

    @property
    @abc.abstractmethod
    def type(self):
        ...


