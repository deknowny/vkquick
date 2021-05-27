from __future__ import annotations

import dataclasses
import datetime
import textwrap
import typing as ty

from vkquick.cached_property import cached_property
from vkquick.chatbot.base.wrapper import Wrapper
from vkquick.chatbot.ui_builders.carousel import Carousel
from vkquick.chatbot.ui_builders.keyboard import Keyboard
from vkquick.chatbot.utils import peer
from vkquick.chatbot.utils import random_id as random_id_
from vkquick.chatbot.wrappers.attachment import Document, Photo
from vkquick.json_parsers import json_parser_policy

if ty.TYPE_CHECKING:
    from vkquick.api import API, PhotoEntityTyping

    AttachmentTyping = ty.Union[str, Photo, Document]
    AttachmentsTyping = ty.Union[ty.List[AttachmentTyping], AttachmentTyping]


class TruncatedMessage(Wrapper):
    @property
    def id(self) -> int:
        return self.fields["message_id"]

    @property
    def peer_id(self) -> int:
        return self.fields["peer_id"]

    @property
    def conversation_message_id(self) -> int:
        return self.fields["conversation_message_id"]

    # Shortcuts
    @property
    def cmid(self) -> int:
        return self.conversation_message_id


class Message(TruncatedMessage):
    @property
    def id(self) -> int:
        return self.fields["id"]

    @cached_property
    def chat_id(self) -> int:
        chat_id = self.peer_id - peer()
        if chat_id < 0:
            raise ValueError(
                "Can't get `chat_id` if message wasn't sent in a chat"
            )

        return chat_id

    @cached_property
    def date(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.fields["date"])

    @property
    def from_id(self) -> int:
        return self.fields["from_id"]

    @property
    def text(self) -> str:
        return self.fields["text"]

    @property
    def random_id(self) -> int:
        return self.fields["random_id"]

    @property
    def attachments(self) -> ty.List[dict]:
        return self.fields["attachments"]

    @property
    def important(self) -> bool:
        return bool(self.fields["important"])

    @property
    def is_hidden(self) -> bool:
        return bool(self.fields["is_hidden"])

    @property
    def out(self) -> bool:
        return bool(self.fields["out"])

    @cached_property
    def keyboard(self) -> ty.Optional[dict]:
        if "keyboard" in self.fields:
            return json_parser_policy.loads(self.fields["keyboard"])
        return None

    @cached_property
    def fwd_messages(self) -> ty.List[Message]:
        return list(map(self.__class__, self.fields["fwd_messages"]))

    @property
    def geo(self) -> ty.Optional[dict]:
        return self.fields.get("geo")

    @cached_property
    def payload(self) -> ty.Optional[dict]:
        if "payload" in self.fields:
            return json_parser_policy.loads(self.fields["payload"])
        return None

    @cached_property
    def reply_message(self) -> ty.Optional[Message]:
        if "reply_message" in self.fields:
            return self.__class__(self.fields["reply_message"])
        return None

    @property
    def action(self) -> dict:
        return self.fields.get("action")

    @property
    def ref(self) -> ty.Optional[str]:
        return self.fields.get("ref")

    @property
    def ref_source(self) -> ty.Optional[str]:
        return self.fields.get("ref_source")

    @property
    def expire_ttl(self) -> ty.Optional[int]:
        return self.fields.get("expire_ttl")

    @cached_property
    def photos(self) -> ty.List[Photo]:
        """
        Возвращает только фотографии из всего,
        что есть во вложениях, оборачивая их в обертку
        """
        photos = [
            Photo(attachment["photo"])
            for attachment in self.attachments
            if attachment["type"] == "photo"
        ]
        return photos

    @cached_property
    def docs(self) -> ty.List[Document]:
        """
        Возвращает только вложения с типом документ из всего,
        что есть во вложениях, оборачивая их в обертку
        """
        docs = [
            Document(attachment["doc"])
            for attachment in self.attachments
            if attachment["type"] == "doc"
        ]
        return docs


@dataclasses.dataclass
class SentMessage:
    api: API
    truncated_message: TruncatedMessage

    async def _send_message(self, params: dict) -> SentMessage:
        # Нужно убрать лишние табы, если такие есть,
        # присутствующие перед каждой строкой
        params["message"] = textwrap.dedent(params["message"]).strip()

        sent_message = await self.api.method("messages.send", **params)
        sent_message = TruncatedMessage(sent_message[0])
        return SentMessage(self.api, sent_message)

    async def upload_photos(
        self, *photos: PhotoEntityTyping
    ) -> ty.List[Photo]:
        """
        Загружает фотографию для отправки в сообщение

        Arguments:
            photos: Фотографии в виде ссылки/пути до файла/сырых байтов/
                IO-хранилища/Path-like объекта

        Returns:
            Список врапперов загруженных фотографий, который можно напрямую
            передать в поле `attachment` при отправке сообщения
        """
        return await self.api.upload_photos_to_message(
            *photos, peer_id=self.truncated_message.peer_id
        )

    async def upload_doc(
        self,
        content: ty.Union[str, bytes],
        filename: str,
        *,
        tags: ty.Optional[str] = None,
        return_tags: ty.Optional[bool] = None,
        type: ty.Literal["doc", "audio_message", "graffiti"] = "doc",
    ) -> Document:
        """
        Загружает документ для отправки в сообщение

        Arguments:
            content: Содержимое документа. Документ может быть
                как текстовым, так и содержать сырые байты
            filename: Имя файла
            tags: Теги для файла, используемые при поиске
            return_tags: Возвращать переданные теги при запросе
            type: Тип документа: файл/голосовое сообщение/граффити

        Returns:
            Враппер загруженного документа. Этот объект можно напрямую
            передать в поле `attachment` при отправке сообщения
        """
        return await self.api.upload_doc_to_message(
            content,
            filename,
            tags=tags,
            return_tags=return_tags,
            type=type,
            peer_id=self.truncated_message.peer_id,
        )

    async def delete(
        self,
        *,
        spam: ty.Optional[bool] = None,
        group_id: ty.Optional[int] = None,
        delete_for_all: bool = True,
    ) -> None:
        """
        Удаляет указанное сообщение (по умолчанию у всех)

        :param spam: Пометить сообщение как спам
        :param group_id: ID группы, от лица которого
            было отправлено сообщение
        :param delete_for_all: Нужно ли удалять сообщение у всех
        """
        if self.truncated_message.id:
            routing = dict(message_ids=self.truncated_message.id)
        else:
            routing = dict(
                conversation_message_ids=self.truncated_message.cmid
            )

        routing["peer_id"] = self.truncated_message.peer_id

        await self.api.method(
            "messages.delete",
            spam=spam,
            group_id=group_id,
            delete_for_all=delete_for_all,
            **routing,
        )

    async def edit(
        self,
        message: str,
        /,
        lat: ty.Optional[float] = None,
        long: ty.Optional[float] = None,
        attachment: ty.Optional[AttachmentsTyping] = None,
        keep_forward_messages: bool = True,
        keep_snippets: bool = True,
        group_id: ty.Optional[int] = None,
        keyboard: ty.Optional[ty.Union[str, Keyboard]] = None,
        dont_parse_links: bool = True,
        template: ty.Optional[ty.Union[str, Carousel]] = None,
    ) -> int:
        if self.truncated_message.id:
            routing = dict(message_id=self.truncated_message.id)
        else:
            routing = dict(
                conversation_message_id=self.truncated_message.cmid
            )

        routing["peer_id"] = self.truncated_message.peer_id

        return await self.api.method(
            "messages.edit",
            message=message,
            lat=lat,
            long=long,
            attachment=attachment,
            keep_forward_messages=keep_forward_messages,
            keep_snippets=keep_snippets,
            group_id=group_id,
            keyboard=keyboard,
            dont_parse_links=dont_parse_links,
            template=template,
            **routing,
        )

    async def reply(
        self,
        message: ty.Optional[str] = None,
        /,
        *,
        random_id: ty.Optional[int] = None,
        lat: ty.Optional[float] = None,
        long: ty.Optional[float] = None,
        attachment: ty.Optional[AttachmentsTyping] = None,
        sticker_id: ty.Optional[int] = None,
        group_id: ty.Optional[int] = None,
        keyboard: ty.Optional[ty.Union[str, Keyboard]] = None,
        template: ty.Optional[ty.Union[str, Carousel]] = None,
        payload: ty.Optional[str] = None,
        dont_parse_links: ty.Optional[bool] = None,
        disable_mentions: bool = True,
        intent: ty.Optional[str] = None,
        expire_ttl: ty.Optional[int] = None,
        silent: ty.Optional[bool] = None,
        subscribe_id: ty.Optional[int] = None,
        content_source: ty.Optional[str] = None,
        **kwargs,
    ) -> SentMessage:
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
            template=template,
            peer_ids=self.truncated_message.peer_id,
            **kwargs,
        )
        if self.truncated_message.id:
            params["reply_to"] = self.truncated_message.id
        else:
            params["forward"] = {
                "is_reply": True,
                "conversation_message_ids": [
                    self.truncated_message.conversation_message_id
                ],
                "peer_id": self.truncated_message.peer_id,
            }
        return await self._send_message(params)

    async def answer(
        self,
        message: ty.Optional[str] = None,
        *,
        random_id: ty.Optional[int] = None,
        lat: ty.Optional[float] = None,
        long: ty.Optional[float] = None,
        attachment: ty.Optional[AttachmentsTyping] = None,
        sticker_id: ty.Optional[int] = None,
        group_id: ty.Optional[int] = None,
        keyboard: ty.Optional[ty.Union[str, Keyboard]] = None,
        payload: ty.Optional[str] = None,
        dont_parse_links: ty.Optional[bool] = None,
        disable_mentions: bool = True,
        template: ty.Optional[ty.Union[str, Carousel]] = None,
        intent: ty.Optional[str] = None,
        expire_ttl: ty.Optional[int] = None,
        silent: ty.Optional[bool] = None,
        subscribe_id: ty.Optional[int] = None,
        content_source: ty.Optional[str] = None,
        **kwargs,
    ) -> SentMessage:
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
            template=template,
            peer_ids=self.truncated_message.peer_id,
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
        attachment: ty.Optional[AttachmentsTyping] = None,
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
        template: ty.Optional[ty.Union[str, Carousel]] = None,
        content_source: ty.Optional[str] = None,
        **kwargs,
    ) -> SentMessage:
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
            template=template,
            peer_ids=self.truncated_message.peer_id,
            **kwargs,
        )
        if self.truncated_message.id:
            params["forward_messages"] = self.truncated_message.id
        else:
            params["forward"] = {
                "conversation_message_ids": [
                    self.truncated_message.conversation_message_id
                ],
                "peer_id": self.truncated_message.peer_id,
            }
        return await self._send_message(params)


class CallbackButtonPressedMessage(Wrapper):
    @property
    def peer_id(self) -> int:
        return self.fields["peer_id"]

    @property
    def user_id(self) -> int:
        return self.fields["user_id"]

    # Alias
    @property
    def from_id(self) -> int:
        return self.user_id

    @property
    def conversation_message_id(self) -> int:
        return self.fields["conversation_message_id"]

    @property
    def event_id(self) -> str:
        return self.fields["event_id"]

    @cached_property
    def payload(self) -> ty.Optional[dict]:
        return self.fields["payload"]

    # Shortcuts
    @property
    def cmid(self) -> int:
        return self.conversation_message_id
