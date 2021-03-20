from __future__ import annotations

import functools
import typing as ty


if ty.TYPE_CHECKING:
    from vkquick.api import API


def api_method(func: ty.Callable[..., ty.Awaitable[None]]):
    @functools.wraps(func)
    async def wrapper(self, **kwargs):
        # `UsersMethod` -> `users`
        method_header = self.__class__.__name__.replace("Method", "").lower()
        method_name = func.__name__
        return await self._api.method(
            f"{method_header}.{method_name}",
            kwargs
        )

    return wrapper


class APIObject:
    def __init__(self, schema: dict) -> None:
        self.__schema__ = schema



class APIMethod:
    def __init__(self, api: API) -> None:
        self._api = api


