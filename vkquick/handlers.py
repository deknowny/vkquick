from __future__ import annotations

import typing as ty

from vkquick.bases.easy_decorator import EasyDecorator

if ty.TYPE_CHECKING:
    pass


class SignalHandler(EasyDecorator):
    def __init__(
        self,
        __handler: ty.Optional[ty.Callable] = None,
        *,
        name: ty.Optional[str] = None
    ):
        self._handler = __handler
        self._name = name or __handler.__name__

    def is_handling_name(self, name: str) -> bool:
        return self._name == name

    def __call__(self, *args, **kwargs):
        return self._handler(*args, **kwargs)


