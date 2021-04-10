from __future__ import annotations

import abc
import typing as ty

from vkquick.api import API
from vkquick.ext.chatbot.providers.base import Provider
from vkquick.ext.chatbot.wrappers.page_entities import Group, PageEntity, User

T = ty.TypeVar("T")
CO_T = ty.TypeVar("CO_T", bound=PageEntity)


class PageEntityProvider(Provider[CO_T], abc.ABC):
    @classmethod
    @abc.abstractmethod
    async def fetch_one(
        cls: ty.Type[T],
        api: API,
        __id,
        *,
        fields: ty.Optional[ty.List[str]] = None
    ) -> T:
        pass

    @classmethod
    @abc.abstractmethod
    async def fetch_many(
        cls: ty.Type[T],
        api: API,
        __id,
        *,
        fields: ty.Optional[ty.List[str]] = None
    ) -> ty.List[T]:
        pass


class UserProvider(PageEntityProvider[User]):
    @classmethod
    async def fetch_one(
        cls, api: API, __id, *, fields: ty.Optional[ty.List[str]] = None
    ) -> UserProvider:
        user = await api.users.get(..., user_ids=__id, fields=fields)
        user = User(user[0])
        return cls(api, user)

    @classmethod
    async def fetch_many(
        cls, api: API, *__ids, fields: ty.Optional[ty.List[str]] = None
    ) -> ty.List[UserProvider]:
        users = await api.users.get(..., user_ids=__ids, fields=fields)
        users = [cls(api, User(user)) for user in users]
        return users


class GroupProvider(PageEntityProvider[Group]):
    @classmethod
    async def fetch_one(
        cls, api: API, __id, *, fields: ty.Optional[ty.List[str]] = None
    ) -> GroupProvider:
        group = await api.groups.get_by_id(..., group_id=__id, fields=fields)
        group = Group(group[0])
        return cls(api, group)

    @classmethod
    async def fetch_many(
        cls, api: API, *__ids, fields: ty.Optional[ty.List[str]] = None
    ) -> ty.List[GroupProvider]:
        groups = await api.groups.get_by_id(
            ..., group_id=__ids, fields=fields
        )
        groups = [cls(api, Group(group)) for group in groups]
        return groups
