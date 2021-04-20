from __future__ import annotations

import abc
import functools
import typing as ty


T = ty.TypeVar("T")


def easy_class_decorator(
    cls: ty.Type[EasyDecorator[T]]
) -> ty.Callable[
    ..., ty.Callable[
        [T], EasyDecorator[T]
    ]
]:
    def args_wrapper(*args, **kwargs) -> ty.Callable[
        [T], EasyDecorator[T]
    ]:
        def handler_wrapper(handler: T) -> EasyDecorator[T]:
            instance = object.__new__(cls)
            instance.handler = handler
            cls.__init__(instance, *args, **kwargs)
            return instance
        return handler_wrapper
    return args_wrapper


class EasyDecorator(ty.Generic[T], abc.ABC):
    """Легкий способ создать класс-декоратор"""

    __handler: ty.Optional[T] = None

    def __init__(self, *args, **kwargs):
        pass

    @property
    def handler(self) -> T:
        if self.__handler is None:
            raise RuntimeError("Can't use handler if the class hasn't been wrapped to a function")
        return self.__handler

    @handler.setter
    def handler(self, value: T) -> None:
        self.__handler = value


class DecoratedFunction(ty.Protocol):
    def __call__(self, handler: T, *args, **kwargs) -> ty.Any:
        pass


F = ty.TypeVar("F", bound=DecoratedFunction)


def easy_func_decorator(func: F) -> F:
    @functools.wraps(func)
    def wrapper_args(*args, **kwargs):
        def wrapper_handler(handler, /):
            return func(handler, *args, **kwargs)
        return wrapper_handler
    return ty.cast(F, wrapper_args)


def easy_method_decorator(func: F) -> F:
    @functools.wraps(func)
    def wrapper_args(self, *args, **kwargs):
        def wrapper_handler(handler, /):
            return func(self, handler, *args, **kwargs)
        return wrapper_handler
    return ty.cast(F, wrapper_args)
