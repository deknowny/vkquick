from __future__ import annotations

import abc
import typing as ty


class BaseMiddleware(abc.ABC):
    @abc.abstractmethod
    async def dispatch(self):
        ...


class MessageMiddleware(BaseMiddleware):
    @abc.abstractmethod
    async def dispatch(self):
        ...


class EventMiddleware(BaseMiddleware):
    @abc.abstractmethod
    async def dispatch(self):
        ...
