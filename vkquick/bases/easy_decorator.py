from __future__ import annotations

import typing as ty


class EasyDecorator:
    """
    Легкий способ создать класс-декоратор
    """
    def __new__(cls, __handler: ty.Optional[ty.Callable] = None, **kwargs) -> EasyDecorator:
        self = object.__new__(cls)
        if __handler is None:
            self.__kwargs = kwargs
            return self.__partail_init
        return self

    def __partail_init(self, __handler: ty.Callable) -> EasyDecorator:
        self.__init__(__handler, **self.__kwargs)
        return self