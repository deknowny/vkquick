from __future__ import annotations

import inspect
import typing as ty

from vkquick.events_generators.event import Event
from vkquick.utils import sync_async_callable, mark_positional_only


class SignalHandler:
    @ty.overload
    @mark_positional_only("handler")
    def __init__(
        self,
        handler: ty.Optional[sync_async_callable(..., ty.Any)] = None,
        *,
        extra_names: ty.Optional[ty.Collection[str]] = None,
    ) -> None:
        ...  # pragma: no cover

    @ty.overload
    @mark_positional_only("handler")
    def __init__(
        self,
        handler: ty.Optional[sync_async_callable(..., ty.Any)] = None,
        *,
        all_names: ty.Optional[ty.Collection[str]] = None,
    ) -> None:
        ...  # pragma: no cover

    @mark_positional_only("handler")
    def __init__(
        self,
        handler: ty.Optional[sync_async_callable(..., ty.Any)] = None,
        *,
        extra_names: ty.Optional[ty.Collection[str]] = None,
        all_names: ty.Optional[ty.Collection[str]] = None,
    ) -> None:
        if extra_names and all_names:
            raise ValueError(
                "Should pass only `extra_names` or `all_names`, not both"
            )

        self._handler = handler
        if extra_names:
            self._names = list(extra_names)
        elif all_names:
            self._names = tuple(all_names)
        else:
            self._names = []
            if handler is not None:
                self(handler)

    def __call__(self, handler: sync_async_callable(..., ty.Any)) -> ty.Any:
        self._handler = handler
        if isinstance(self._names, list):
            self._names.append(handler.__name__)

        return self

    def call(self, *args, **kwargs) -> ty.Any:
        return self._handler(*args, **kwargs)

    def is_handling_name(self, name: str) -> bool:
        return name in self._names

    @property
    def handler(self) -> sync_async_callable(..., ty.Any):
        return self._handler


class EventHandler(SignalHandler):
    @ty.overload
    @mark_positional_only("handler")
    def __init__(
        self,
        handler: ty.Optional[sync_async_callable(..., ty.Any)] = None,
        *,
        extra_types: ty.Optional[ty.Collection[str]] = None,
    ) -> None:
        ...  # pragma: no cover

    @ty.overload
    @mark_positional_only("handler")
    def __init__(
        self,
        handler: ty.Optional[sync_async_callable(..., ty.Any)] = None,
        *,
        all_types: ty.Optional[ty.Collection[str]] = None,
    ) -> None:
        ...  # pragma: no cover

    @ty.overload
    @mark_positional_only("handler")
    def __init__(
        self,
        handler: ty.Optional[sync_async_callable(..., ty.Any)] = None,
        *,
        handle_every_event: bool = False,
    ) -> None:
        ...  # pragma: no cover

    @mark_positional_only("handler")
    def __init__(
        self,
        handler: ty.Optional[sync_async_callable(..., ty.Any)] = None,
        *,
        extra_types: ty.Optional[ty.Collection[str]] = None,
        all_types: ty.Optional[ty.Collection[str]] = None,
        handle_every_event: bool = False,
    ) -> None:
        super().__init__(  # noqa
            handler, extra_names=extra_types, all_names=all_types
        )
        if handle_every_event and (extra_types or all_types):
            raise ValueError(
                "Should use only `handle_every_event` "
                "or `extra_types` or `all_types`"
            )

        self._handle_every_event = handle_every_event

    def call(self, event: Event) -> ty.Any:
        if self._pass_event:
            return self._handler(event)
        return self._handler()

    def __call__(self, handler: sync_async_callable(..., ty.Any)) -> ty.Any:
        parameters = inspect.signature(handler).parameters
        self._pass_event = len(parameters) == 1
        if len(parameters) not in (0, 1):
            raise TypeError(
                f"Event handler should" f"take only 1 or 0 arguments"
            )

        return super().__call__(handler)

    def is_handling_name(self, name: str) -> bool:
        return super().is_handling_name(name) or self._handle_every_event
