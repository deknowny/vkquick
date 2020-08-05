import typing
import inspect


T = typing.TypeVar("T")


async def run(result: typing.Union[T, typing.Awaitable[T]]) -> T:
    """
    Returns value or execute awaitable object.
    """
    if inspect.isawaitable(result):
        return await result
    return result
