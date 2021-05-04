from __future__ import annotations

import abc
import asyncio
import dataclasses
import typing as ty


CallNext = ty.Callable[[], ty.Awaitable]
ContextTypevar = ty.TypeVar("ContextTypevar")


def call_next_drop(
    call_next: asyncio.Event,
    rollback: asyncio.Event
):
    async def wrapper():
        rollback.set()
        await call_next.wait()

    return wrapper


class BaseMiddleware(abc.ABC, ty.Generic[ContextTypevar]):
    @abc.abstractmethod
    async def dispatch(self, ctx: ContextTypevar, call_next: CallNext):
        ...

    async def run_dispatch(
        self,
        ctx: ContextTypevar,
        call_next: asyncio.Event,
        rollback: asyncio.Event
    ):
        mocked_call_next = call_next_drop(call_next, rollback)
        await self.dispatch(ctx, mocked_call_next)

        # Если call_next не было вызван,
        # все равно нужно сообщить о том,
        # что вызов завершен
        rollback.set()


class Dispatcher:

    def __init__(
        self, middlewares: ty.List[BaseMiddleware[ContextTypevar]], context: ContextTypevar
    ):
        self._middlewares = middlewares
        self._context = context
        self._active_middlewares_calls = []

    async def foreword(self) -> bool:
        for middleware in self._middlewares:
            call_next = asyncio.Event()
            rollback = asyncio.Event()
            dispatch_task = asyncio.create_task(
                middleware.run_dispatch(self._context, call_next, rollback)
            )
            # Ожидание, когда мидлвар передаст управление
            await rollback.wait()

            # Ожидается ли call_next внутри вызова
            if not len(call_next._waiters):  # noqa
                return False

            self._active_middlewares_calls.append((call_next, dispatch_task))

        return True

    async def afterword(self):
        for middleware_call, dispatch_task in reversed(self._active_middlewares_calls):
            middleware_call.set()
            await dispatch_task


@dataclasses.dataclass
class MiddlewareWrapper(BaseMiddleware[CallNext]):

    callback: ty.Callable[[ContextTypevar, CallNext], ty.Awaitable]

    async def dispatch(self, ctx: ContextTypevar, call_next: CallNext):
        return await self.callback(ctx, call_next)

