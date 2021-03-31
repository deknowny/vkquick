from __future__ import annotations

import datetime
import typing as ty

from vkquick.ext.chatbot.wrappers.base import Wrapper
from vkquick.ext.chatbot.utils import peer
from vkquick.cached_property import cached_property
from vkquick.ext.chatbot.wrappers.attachment import Document, Photo
from vkquick.json_parsers import json_parser_policy


class Message(Wrapper):
    @property
    def id(self) -> int:
        return self.fields["id"]

    @property
    def peer_id(self) -> int:
        return self.fields["peer_id"]

    @cached_property
    def chat_id(self) -> int:
        chat_id = self.peer_id - peer()
        if chat_id < 0:
            raise ValueError(
                "Can't get `chat_id` if message " "wasn't sent in a chat"
            )

        return chat_id

    @property
    def conversation_message_id(self) -> int:
        return self.fields["conversation_message_id"]

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

    # Shortcuts
    @property
    def cmid(self) -> int:
        return self.conversation_message_id
