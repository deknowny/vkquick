import asyncio
import typing as ty

T = ty.TypeVar("T")


OptionalAwaitable = ty.Union[ty.Awaitable[T], T]


async def sync_async_run(__obj: OptionalAwaitable) -> ty.Union[T, ty.Any]:
    """
    Позволяет вызывать корутины и обычные функции под одним интерфейсом
    Если переданное значение является корутиной,
    то к ней применится `await`, иначе вернется переданное значение,
    т.к. функция была синхронной и вызов уже прошел

    :return: Возвращаемое корутиной значение или само значение
    """
    if asyncio.iscoroutine(__obj):
        return await __obj
    return __obj
