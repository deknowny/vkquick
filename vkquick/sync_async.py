import asyncio
import typing as ty

T = ty.TypeVar("T")


def sync_async_callable(
    args: ty.Union[ty.List[ty.Any], type(...)], returns: ty.Any = ty.Any
) -> ty.Type[ty.Callable]:
    """
    Позволяет собрать корректный тайпинг для синхронных и асинхронных функций

    :param args: Аргументы, принимаемые корутинной или обычной функцией
    :param returns: Значение, возвращаемое корутинной или обычной функцией
    :return: Корректный тайпинг для асинхронной/асинхронной функции
    """
    if args is not Ellipsis:
        return ty.Callable[
            [*args],
            ty.Union[ty.Awaitable[returns], returns],
        ]

    return ty.Callable[
        ...,
        ty.Union[ty.Awaitable[returns], returns],
    ]


async def sync_async_run(
    __obj: ty.Union[T, ty.Awaitable]
) -> ty.Union[T, ty.Any]:
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
