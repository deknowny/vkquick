from __future__ import annotations

import abc
import typing as ty

if ty.TYPE_CHECKING:
    from vkquick.bot import EventProcessingContext


class Middleware(abc.ABC):
    @abc.abstractmethod
    async def foreword(self, epctx: EventProcessingContext):
        ...

    @abc.abstractmethod
    async def afterword(self, epctx: EventProcessingContext):
        ...
