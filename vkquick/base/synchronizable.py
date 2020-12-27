from __future__ import annotations

import dataclasses
import functools
import typing as ty


class Synchronizable:
    """
    Протокол для синхронизации объектов

    Некоторое поведение объектов может быть
    асинхронным (например, вызов API методов),
    но использовать те же возможности, когда весь код строится
    синхронно и конкурировать нечему, не нужно.
    Поэтому этот класс определяет общее поведение для
    объектов, чье поведение должно стать синхронным.
    """

    __synchronized = False  # По умолчанию асинхронно

    @property
    def is_synchronized(self):
        """
        Состояние режима объекта: асинхронный/синхронный
        """
        return self.__synchronized

    def synchronize(self):
        """
        Метод, меняющий поведение на синхронное.
        Если вы меняете поведение разово, используйте
        вместе с менеджером контекста:

            with obj.synchronize():
                obj.some_method_that_was_async_but_now_sync()
        """
        self.__synchronized = True
        return self

    def __enter__(self):
        """
        Менеджер контекста гарантирует, что
        поведение объекта обратно поменяется на асинхронное
        """

    def __exit__(self, *args):
        self.__synchronized = False


def synchronizable_function(func) -> _SynchronizableFunction:
    return _SynchronizableFunction(async_func=func)


@dataclasses.dataclass
class _SynchronizableFunction:

    async_func: ty.Callable[
        ..., ty.Awaitable[ty.Any],
    ]
    sync_func: ty.Optional[ty.Callable[..., ty.Any]] = None

    def __get__(self, instance, owner):
        if instance.is_synchronized:
            return functools.partial(self.sync_func, instance)
        return functools.partial(self.async_func, instance)

    def sync_edition(self, func: ty.Callable[..., ty.Any]) -> _SynchronizableFunction:
        self.sync_func = func
        return self
