import typing as ty

from vkquick.api import API
from vkquick.ext.chatbot.wrappers.page_entities import PageEntity, Group, User


class LiteAPI:
    def __init__(self, api: API) -> None:
        self._api = api

    async def fetch_user(
        self, __id, *, fields: ty.Optional[ty.List[str]] = None
    ) -> User:
        user = await self._api.users.get(..., user_ids=__id, fields=fields)
        user = User(user[0])
        return user

    async def fetch_users(
        self, *__ids, fields: ty.Optional[ty.List[str]] = None
    ) -> ty.List[User]:
        users = await self._api.users.get(..., user_ids=__ids, fields=fields)
        users = list(map(User, users))
        return users

    async def fetch_group(self, __id, *, fields: ty.Optional[ty.List[str]] = None) -> Group:
        group = await self._api.groups.get_by_id(..., group_id=__id, fields=fields)
        group = Group(group[0])
        return group

    async def fetch_groups(self, *__ids,  fields: ty.Optional[ty.List[str]] = None) -> ty.List[Group]:
        groups = await self._api.groups.get_by_id(..., group_id=__ids, fields=fields)
        groups = list(map(Group, groups))
        return groups
