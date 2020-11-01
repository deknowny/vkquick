from __future__ import annotations
import dataclasses
import enum
import typing as ty

import vkquick.utils


class ReservedSignal(enum.Enum):
    STARTUP = enum.auto()
    SHUTDOWN = enum.auto()
    POST_EVENT_HANDLING = enum.auto()


SignalName = ty.Union[str, ReservedSignal]


@dataclasses.dataclass
class SignalHandler:

    name: SignalName

    def __call__(
        self, reaction: vkquick.utils.sync_async_callable(..., ty.Any)
    ) -> SignalHandler:
        self.reaction = reaction
        return self


@dataclasses.dataclass
class SignalCaller:
    handlers: ty.List[SignalHandler] = dataclasses.field(default_factory=list)
    signal_name: ty.Optional[SignalName] = None

    def __getattr__(self, signal_name: SignalName) -> SignalCaller:
        self.signal_name = signal_name
        return self

    def __call__(self, *args, **kwargs) -> ty.Any:
        signal_name = self.signal_name
        self.signal_name = None
        for handler in self.handlers:
            if handler.name == signal_name:
                return vkquick.utils.sync_async_run(
                    handler.reaction(*args, **kwargs)
                )
