from __future__ import annotations
import typing as ty

from vkquick.utils import sync_async_callable
from vkquick.events_generators.event import Event


class SignalHandler:
    @ty.overload
    def __init__(
        self,
        handler: ty.Optional[
            sync_async_callable(..., ty.Any)
        ] = None, /, *,
        extra_names: ty.Optional[ty.Collection[str]] = None,
    ) -> None:
        ...

    @ty.overload
    def __init__(
        self,
        handler: ty.Optional[
            sync_async_callable(..., ty.Any)
        ] = None, /, *,
        all_names: ty.Optional[ty.Collection[str]] = None,
    ) -> None:
        ...

    def __init__(
        self,
        handler: ty.Optional[
            sync_async_callable(..., ty.Any)
        ] = None, /, *,
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
            self._names = extra_names
        else:
            if handler is None:
                raise ValueError("Should pass a handler or handled names")
            self._names = [handler.__name__]
            
    def __call__(self, handler: sync_async_callable(..., ty.Any)) -> ty.Any:
        self._handler = handler
        if isinstance(self._names, list):
            self._names.append(handler.__name__)

    def call(self, *args, **kwargs) -> ty.Any:
        return self._handler(*args, **kwargs)

    def is_handling_name(self, name: str) -> bool:
        return name in self._names


class EventHandler(SignalHandler):

    @ty.overload
    def __init__(
        self,
        handler: ty.Optional[
            sync_async_callable(..., ty.Any)
        ] = None, /, *,
        extra_types: ty.Optional[ty.Collection[str]] = None,
    ) -> None:
        ...

    @ty.overload
    def __init__(
        self,
        handler: ty.Optional[
            sync_async_callable(..., ty.Any)
        ] = None, /, *,
        all_types: ty.Optional[ty.Collection[str]] = None,
    ) -> None:
        ...

    @ty.overload
    def __init__(
        self,
        handler: ty.Optional[
            sync_async_callable(..., ty.Any)
        ] = None, /, *,
        handle_every_event: bool = False
    ) -> None:
        ...

    def __init__(
        self,
        handler: ty.Optional[
            sync_async_callable(..., ty.Any)
        ] = None, /, *,
        extra_types: ty.Optional[ty.Collection[str]] = None,
        all_types: ty.Optional[ty.Collection[str]] = None,
        handle_every_event: bool = False
    ) -> None:
        super().__init__(  # noqa
            handler,
            extra_names=extra_types,
            all_names=all_types
        )
        if handle_every_event and (extra_types or all_types):
            raise ValueError(
                "Should use only `handle_every_event` "
                "or `extra_types` or `all_types`"
            )

        self._handle_every_event = handle_every_event

    def call(self, event: Event) -> ty.Any:
        return self._handler(event)

    def is_handling_name(self, name: str) -> bool:
        return super().is_handling_name(name) or self._handle_every_event