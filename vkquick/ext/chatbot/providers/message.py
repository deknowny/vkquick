from __future__ import annotations

import asyncio
import dataclasses
import typing as ty

from vkquick.ext.chatbot.providers.attachment import (
    PhotoProvider,
)
from vkquick.ext.chatbot.providers.base import Provider
from vkquick.ext.chatbot.providers.page_entity import (
    GroupProvider,
    PageEntityProvider,
    UserProvider,
)
from vkquick.ext.chatbot.ui_builders.keyboard import Keyboard
from vkquick.ext.chatbot.utils import random_id as random_id_
from vkquick.ext.chatbot.wrappers import Photo
from vkquick.ext.chatbot.wrappers.message import Message, TruncatedMessage

T = ty.TypeVar("T", bound=TruncatedMessage)


@dataclasses.dataclass
class _LazyMessageResponseStorage:
    mp: AnyMessageProvider
    attached_photos: ty.List[ty.Union[bytes, str]] = dataclasses.field(
        default_factory=list
    )
    downloaded_photos: ty.List[Photo] = dataclasses.field(
        default_factory=list
    )

    async def fetch_new_fields(self) -> dict:
        new_fields = {
            "attachment": []  # Если пустой, то впоследствии удалится
        }
        # Attached photos
        if len(self.attached_photos) > 10:
            raise ValueError("Can't upload more than 10 photos")
        elif len(self.attached_photos) > 5:
            first_part = self.attached_photos[:6]
            second_part = self.attached_photos[5:]
            first_part_photos, second_part_photos = await asyncio.gather(
                self.mp.upload_photos(*first_part),
                self.mp.upload_photos(*second_part),
            )
            photos = [*first_part_photos, *second_part_photos]
            new_fields["attachment"].extend(photo.storage for photo in photos)
        elif len(self.attached_photos):
            photos = await self.mp.upload_photos(*self.attached_photos)
            new_fields["attachment"].extend(photo.storage for photo in photos)

        # Downloaded photos
        if len(self.downloaded_photos):
            new_fields["attachment"].extend(self.downloaded_photos)

        # Если нет вложений, то удаляем поле с вложениями
        if not new_fields["attachment"]:
            del new_fields["attachment"]

        return new_fields


class AnyMessageProvider(Provider[T]):
    def __init__(self, *args, **kwargs):
        Provider.__init__(self, *args, **kwargs)
        self._response_storage = _LazyMessageResponseStorage(mp=self)

    async def _send_message(self, params: dict) -> TruncatedMessageProvider:
        new_fields = await self._response_storage.fetch_new_fields()
        params.update(new_fields)
        sent_message = await self._api.method("messages.send", params)
        return TruncatedMessageProvider.from_mapping(
            api=self._api, storage=sent_message[0]
        )

    def attach_photos(
        self, *photos: ty.Union[bytes, str, Photo, PhotoProvider]
    ) -> None:
        for photo in photos:
            if isinstance(photo, (str, bytes)):
                self._response_storage.attached_photos.append(photo)
            elif isinstance(photo, Photo):
                self._response_storage.downloaded_photos.append(photo)
            elif isinstance(photo, PhotoProvider):
                self._response_storage.downloaded_photos.append(photo.storage)

    def attach_photo(
        self, photo: ty.Union[bytes, str, Photo, PhotoProvider]
    ) -> None:
        self.attach_photos(photo)

    async def upload_photos(
        self, *photos: ty.Union[bytes, str], attach_to_response: bool = False
    ) -> ty.List[PhotoProvider]:
        photos = await PhotoProvider.upload_many_to_message(
            *photos, api=self._api, peer_id=self.storage.peer_id
        )
        if attach_to_response:
            self._response_storage.downloaded_photos.extend(
                photo.storage for photo in photos
            )
        return photos

    async def upload_photo(
        self, photo: ty.Union[bytes, str], attach_to_response: bool = False
    ) -> PhotoProvider:
        photos = await self.upload_photos(
            photo, attach_to_response=attach_to_response
        )
        return photos[0]

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
        keyboard: ty.Optional[ty.Union[str, Keyboard]] = None,
        payload: ty.Optional[str] = None,
        dont_parse_links: ty.Optional[bool] = None,
        disable_mentions: bool = True,
        intent: ty.Optional[str] = None,
        expire_ttl: ty.Optional[int] = None,
        silent: ty.Optional[bool] = None,
        subscribe_id: ty.Optional[int] = None,
        content_source: ty.Optional[str] = None,
        **kwargs,
    ) -> TruncatedMessageProvider:
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

    async def answer(
        self,
        message: ty.Optional[str] = None,
        *,
        random_id: ty.Optional[int] = None,
        lat: ty.Optional[float] = None,
        long: ty.Optional[float] = None,
        attachment: ty.Optional[ty.List[ty.Union[str]]] = None,
        sticker_id: ty.Optional[int] = None,
        group_id: ty.Optional[int] = None,
        keyboard: ty.Optional[ty.Union[str, Keyboard]] = None,
        payload: ty.Optional[str] = None,
        dont_parse_links: ty.Optional[bool] = None,
        disable_mentions: bool = True,
        intent: ty.Optional[str] = None,
        expire_ttl: ty.Optional[int] = None,
        silent: ty.Optional[bool] = None,
        subscribe_id: ty.Optional[int] = None,
        content_source: ty.Optional[str] = None,
        **kwargs,
    ) -> TruncatedMessageProvider:
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
        return await self._send_message(params)

    async def forward(
        self,
        message: ty.Optional[str] = None,
        *,
        random_id: ty.Optional[int] = None,
        lat: ty.Optional[float] = None,
        long: ty.Optional[float] = None,
        attachment: ty.Optional[ty.List[ty.Union[str]]] = None,
        sticker_id: ty.Optional[int] = None,
        group_id: ty.Optional[int] = None,
        keyboard: ty.Optional[ty.Union[str, Keyboard]] = None,
        payload: ty.Optional[str] = None,
        dont_parse_links: ty.Optional[bool] = None,
        disable_mentions: bool = True,
        intent: ty.Optional[str] = None,
        expire_ttl: ty.Optional[int] = None,
        silent: ty.Optional[bool] = None,
        subscribe_id: ty.Optional[int] = None,
        content_source: ty.Optional[str] = None,
        **kwargs,
    ) -> TruncatedMessageProvider:
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
            params["forward_messages"] = self.storage.id
        else:
            params["forward"] = {
                "conversation_message_ids": [
                    self.storage.conversation_message_id
                ],
                "peer_id": self.storage.peer_id,
            }
        return await self._send_message(params)


class TruncatedMessageProvider(AnyMessageProvider[TruncatedMessage]):
    async def extend(self) -> MessageProvider:
        if self.storage["message_id"] == 0:
            message = await self._api.messages.get_by_conversation_message_id(
                peer_id=self.storage.peer_id,
                conversation_message_ids=self.storage.conversation_message_id,
            )
            return MessageProvider.from_mapping(
                api=self._api, storage=message["items"][0]
            )

        else:
            message = await self._api.messages.get_by_id(
                message_ids=self.storage["message_id"]
            )
            return MessageProvider.from_mapping(
                api=self._api, storage=message["items"][0]
            )


class MessageProvider(AnyMessageProvider[Message]):
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
            return await UserProvider.fetch_one(
                self._api, self._storage.from_id
            )

    async def fetch_group_sender(self) -> GroupProvider:
        if self._storage.from_id > 0:
            raise ValueError(
                "Message was sent by a user. Can't fetch group provider"
            )
        else:
            return await GroupProvider.fetch_one(
                self._api, self._storage.from_id
            )
