from __future__ import annotations

import typing as ty

if ty.TYPE_CHECKING:
    from vkquick.bot import EventProcessingContext


class Middleware:
    """
    Мидлвар — сущность, содержащая методы, которые
    будут вызваны перед тем, как начать обработку
    события обработчиками событий и после того,
    как все обработчики события были вызваны
    """
    async def foreword(self, epctx: EventProcessingContext) -> None:
        """
        Вызывается перед тем, как начать обработку

        Arguments:
            epctx: Контекст процесса обработки события
        """

    async def afterword(self, epctx: EventProcessingContext) -> None:
        """
        Вызывается после того, как закончится обработка события

        Arguments:
            epctx: Контекст процесса обработки события
        """
