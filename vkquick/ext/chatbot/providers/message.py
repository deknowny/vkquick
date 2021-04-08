from __future__ import annotations

import functools
import typing as ty

from vkquick.ext.chatbot.utils import random_id as random_id_
from vkquick.ext.chatbot.providers.base import Provider
from vkquick.ext.chatbot.providers.page_entity import (
    GroupProvider,
    PageEntityProvider,
    UserProvider,
)
from vkquick.ext.chatbot.wrappers.message import Message


def message_send_method(func) -> ty.Callable[..., ty.Awaitable]:
    @functools.wraps(func)
    async def wrapper(self: MessageProvider, *args, **kwargs):
        custom_params = await func(self, *args, **kwargs)

        kwargs.update(peer_ids=self.storage.peer_id)
        kwargs.update(
            random_id=random_id_()
            if kwargs["random_id"] is None
            else kwargs["random_id"]
        )
        if args:
            kwargs["message"] = args[0]
        kwargs.update(custom_params)

        return await self._send_message(kwargs)

    return wrapper


class MessageProvider(Provider[Message]):
    async def _send_message(self, params: dict):
        await self._api.method("messages.send", params)

    # Если использовать декоратор, чтобы получить все эти параметры как `kwargs`,
    # то по непонятным причинам pycharm распознает этот метод не как callable-объект.
    # Чего только не сделаешь ради удобных автокомплитов...
    async def reply(
        self,
        message: ty.Optional[str] = None,
        *,
        random_id: ty.Optional[int] = None,
        lat: ty.Optional[float] = None,
        long: ty.Optional[float] = None,
        attachment: ty.Optional[ty.List[ty.Union[str]]] = None,
        sticker_id: ty.Optional[int] = None,
        group_id: ty.Optional[int] = None,
        keyboard: ty.Optional[ty.Union[str]] = None,
        payload: ty.Optional[str] = None,
        dont_parse_links: ty.Optional[bool] = None,
        disable_mentions: bool = True,
        intent: ty.Optional[str] = None,
        expire_ttl: ty.Optional[int] = None,
        silent: ty.Optional[bool] = None,
        subscribe_id: ty.Optional[int] = None,
        content_source: ty.Optional[str] = None,
        **kwargs,
    ):
        params = dict(
            message=message,
            random_id=random_id_() if random_id is None else random_id,
            lat=lat,
            long=long,
            attachment=attachment,
            sticker_id=sticker_id,
            group_id=group_id,
            keyboard=keyboard,
            payload=payload,
            dont_parse_links=dont_parse_links,
            disable_mentions=disable_mentions,
            intent=intent,
            expire_ttl=expire_ttl,
            silent=silent,
            subscribe_id=subscribe_id,
            content_source=content_source,
            peer_ids=self.storage.peer_id,
            **kwargs,
        )
        if self.storage.id:
            params["reply_to"] = self.storage.id
        else:
            params["forward"] = {
                "is_reply": True,
                "conversation_message_ids": [
                    self.storage.conversation_message_id
                ],
                "peer_id": self.storage.peer_id,
            }
        return await self._send_message(params)

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
