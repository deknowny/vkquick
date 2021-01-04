from __future__ import annotations
import datetime
import functools
import json
import typing as ty

from vkquick.wrappers.attachment import Photo, Document
from vkquick.utils import AttrDict, peer
from vkquick.base.wrapper import Wrapper


class Message(Wrapper):
    @property
    def id(self) -> int:
        return self.fields.id

    @property
    def peer_id(self) -> int:
        return self.fields.peer_id

    @functools.cached_property
    def chat_id(self) -> int:
        chat_id = self.peer_id - peer()
        if chat_id < 0:
            raise ValueError(
                "Can't get `chat_id` if message wasn't sent in a chat"
            )

        return chat_id

    @property
    def conversation_message_id(self) -> int:
        return self.fields.conversation_message_id

    @functools.cached_property
    def date(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.fields.date)

    @property
    def from_id(self) -> int:
        return self.fields.from_id

    @property
    def text(self) -> str:
        return self.fields.text

    @property
    def random_id(self) -> int:
        return self.fields.random_id

    @property
    def attachments(self) -> ty.List[AttrDict]:
        return list(self.fields.attachments)

    @property
    def important(self) -> bool:
        return bool(self.fields.important)

    @property
    def is_hidden(self) -> bool:
        return bool(self.fields.important)

    @property
    def out(self) -> bool:
        return bool(self.fields.out)

    @functools.cached_property
    def keyboard(self) -> ty.Optional[AttrDict]:
        if "keyboard" in self.fields:
            return AttrDict(json.loads(self.fields.keyboard))
        return None

    @functools.cached_property
    def fwd_messages(self) -> ty.List[Message]:
        return list(map(self.__class__, self.fields.fwd_messages))

    @property
    def geo(self) -> ty.Optional[AttrDict]:
        return self.fields.geo if "geo" in self.fields else None

    @functools.cached_property
    def payload(self) -> ty.Optional[AttrDict]:
        if "payload" in self.fields:
            return AttrDict(json.loads(self.fields.payload))
        return None

    @functools.cached_property
    def reply_message(self) -> ty.Optional[Message]:
        if "reply_message" in self.fields:
            return self.__class__(self.fields.reply_message)
        return None

    @property
    def action(self) -> ty.Optional[AttrDict]:
        return self.fields.action if "action" in self.fields else None

    @property
    def ref(self) -> ty.Optional[str]:
        return self.fields.ref if "ref" in self.fields else None

    @property
    def ref_source(self) -> ty.Optional[str]:
        return self.fields.ref_source if "ref_source" in self.fields else None

    @property
    def expire_ttl(self) -> ty.Optional[int]:
        return self.fields.expire_ttl if "expire_ttl" in self.fields else None

    @functools.cached_property
    def photos(self) -> ty.List[Photo]:
        """
        Возвращает только фотографии из всего,
        что есть во вложениях, оборачивая их в обертку
        """
        photos = [
            Photo(attachment.photo)
            for attachment in self.attachments
            if attachment.type == "photo"
        ]
        return photos

    @functools.cached_property
    def docs(self):
        """
        Возвращает только вложения с типом документ из всего,
        что есть во вложениях, оборачивая их в обертку
        """
        docs = [
            Document(attachment.doc)
            for attachment in self.attachments
            if attachment.type == "doc"
        ]
        return docs

    # Shortcuts
    cmid = conversation_message_id
