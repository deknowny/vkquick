from __future__ import annotations

import typing as ty

from vkquick.api import API

T = ty.TypeVar("T")


class Provider(ty.Generic[T]):
    def __init__(self, api: API, storage: T) -> None:
        self._api: API = api
        self._storage: T = storage

    @classmethod
    def from_wrapper(cls, api: API, storage: T) -> Provider:
        return cls(api, storage)

    @classmethod
    def from_mapping(cls, api: API, storage: dict) -> Provider:
        type_from_generic = cls.__orig_bases__[0].__args__[0]
        return cls(api, type_from_generic(storage))

    @property
    def storage(self) -> T:
        return self._storage

    def __repr__(self):
        return f"""{self.__class__.__name__}(api={self._api}, storage={self._storage!r})"""
