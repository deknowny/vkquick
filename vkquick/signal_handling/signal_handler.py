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
