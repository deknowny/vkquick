from __future__ import annotations
import dataclasses
import typing as ty

import vkquick.utils


@dataclasses.dataclass
class SignalHandler:
    signal_name: str

    def __call__(self, reaction: ty.Callable[..., ty.Any]) -> SignalHandler:
        self.reaction = reaction
        return self

    # async def handle_signal(self, signal_name: str, *args, **kwargs) -> ty.Any:
    #     return await vkquick.utils.sync_async_run(self.reaction(*args, **kwargs))
    #
