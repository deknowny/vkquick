from __future__ import annotations

import abc
import functools
import typing as ty


class EasyDecorator(abc.ABC):
    """Легкий способ создать класс-декоратор"""

    def __new__(
        cls, handler: ty.Optional[ty.Callable] = None, /, **kwargs
    ) -> ty.Union[EasyDecorator, ty.Callable[..., EasyDecorator]]:
        self = object.__new__(cls)
        if handler is None:
            self.__kwargs = kwargs
            return self.__partail_init
        return self

    def __partail_init(self, handler: ty.Callable, /) -> EasyDecorator:
        self.__init__(handler, **self.__kwargs)
        return self


def easy_func_decorator(func: ty.Callable):
    """

    Args:
      func: ty.Callable:
      func: ty.Callable:

    Returns:

    """

    @functools.wraps(func)
    def wrapper_args(handler: ty.Optional[ty.Callable] = None, /, **kwargs):
        """

        Args:
          handler: ty.Optional[ty.Callable]:  (Default value = None)
          **kwargs:
          handler: ty.Optional[ty.Callable]:  (Default value = None)

        Returns:

        """
        if handler is None:

            def wrapper_handler(handler: ty.Callable, /):
                """

                Args:
                  handler: ty.Callable:
                  handler: ty.Callable:

                Returns:

                """
                return func(handler, **kwargs)

            return wrapper_handler
        return func(handler, **kwargs)

    return wrapper_args


def easy_method_decorator(func: ty.Callable):
    """

    Args:
      func: ty.Callable:
      func: ty.Callable:

    Returns:

    """

    @functools.wraps(func)
    def wrapper_args(
        self, handler: ty.Optional[ty.Callable] = None, /, **kwargs
    ):
        """

        Args:
          handler: ty.Optional[ty.Callable]:  (Default value = None)
          **kwargs:
          handler: ty.Optional[ty.Callable]:  (Default value = None)

        Returns:

        """
        if handler is None:

            def wrapper_handler(handler: ty.Callable, /):
                """

                Args:
                  handler: ty.Callable:
                  handler: ty.Callable:

                Returns:

                """
                return func(self, handler, **kwargs)

            return wrapper_handler
        return func(self, handler, **kwargs)

    return wrapper_args
