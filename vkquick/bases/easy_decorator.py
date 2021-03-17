from __future__ import annotations

import abc
import functools
import typing as ty


class EasyDecorator(abc.ABC):
    """
    Легкий способ создать класс-декоратор
    """

    def __new__(cls, __handler: ty.Optional[ty.Callable] = None, **kwargs):
        self = object.__new__(cls)
        if __handler is None:
            self.__kwargs = kwargs
            return self.__partail_init
        return self

    def __partail_init(self, __handler: ty.Callable) -> EasyDecorator:
        self.__init__(__handler, **self.__kwargs)
        return self


def easy_func_decorator(func: ty.Callable):
    @functools.wraps(func)
    def wrapper_args(__handler: ty.Optional[ty.Callable] = None, **kwargs):
        if __handler is None:

            def wrapper_handler(__handler: ty.Callable):
                return func(__handler, **kwargs)

            return wrapper_handler
        return func(__handler, **kwargs)

    return wrapper_args


def easy_method_decorator(func: ty.Optional[ty.Callable]):
    @functools.wraps(func)
    def wrapper_args(
        self, __handler: ty.Optional[ty.Callable] = None, **kwargs
    ):
        if __handler is None:

            def wrapper_handler(__handler: ty.Callable):
                return func(self, __handler, **kwargs)

            return wrapper_handler
        return func(self, __handler, **kwargs)

    return wrapper_args
