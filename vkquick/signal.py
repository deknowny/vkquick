from __future__ import annotations

import typing as ty

from loguru import logger

from vkquick.bases.easy_decorator import EasyDecorator


class SignalHandler(EasyDecorator):
    def __init__(
        self,
        __handler: ty.Optional[ty.Callable] = None,
        *,
        name: ty.Optional[str] = None
    ):
        self._handler = __handler
        self._name = name or __handler.__name__

    @property
    def name(self):
        return self._name

    def is_handling_name(self, name: str) -> bool:
        return self._name == name

    def __call__(self, *args, **kwargs):
        logger.info(
            "Call signal {name} with args={args} and kwargs={kwargs}",
            name=self._name,
            args=args,
            kwargs=kwargs,
        )
        return self._handler(*args, **kwargs)
