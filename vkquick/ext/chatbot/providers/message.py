from vkquick.ext.chatbot.providers.base import Provider
from vkquick.ext.chatbot.providers.page_entity import (
    GroupProvider,
    PageEntityProvider,
    UserProvider,
)
from vkquick.ext.chatbot.wrappers.message import Message


class MessageProvider(Provider[Message]):
    async def fetch_any_sender(self) -> PageEntityProvider:
        if self._storage.from_id > 0:
            return await UserProvider.fetch_one(
                self._api, self._storage.from_id
            )
        else:
            return await GroupProvider.fetch_one(
                self._api, self._storage.from_id
            )

    async def fetch_user_sender(self) -> UserProvider:
        if self._storage.from_id < 0:
            raise ValueError(
                "Message was sent by a group. Can't fetch user provider"
            )
        else:
            return await self._api.fetch_user(self._storage.from_id)

    async def fetch_group_sender(self) -> GroupProvider:
        if self._storage.from_id > 0:
            raise ValueError(
                "Message was sent by a user. Can't fetch group provider"
            )
        else:
            return await self._api.fetch_group(self._storage.from_id)
