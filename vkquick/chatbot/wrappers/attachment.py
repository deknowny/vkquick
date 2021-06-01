from __future__ import annotations

import typing

import aiohttp

from vkquick.base.api_serializable import APISerializableMixin
from vkquick.chatbot.base.wrapper import Wrapper
from vkquick.chatbot.utils import download_file


class Attachment(Wrapper, APISerializableMixin):
    """
    Базовый класс для всех attachment-типов
    """

    _name = None

    def represent_as_api_param(self) -> str:
        if "access_key" in self.fields:
            access_key = f"""_{self.fields["access_key"]}"""
        else:
            access_key = ""

        return "{type}{owner_id}_{attachment_id}{access_key}".format(
            type=self._name,
            owner_id=self.fields["owner_id"],
            attachment_id=self.fields["id"],
            access_key=access_key,
        )


class Photo(Attachment):
    _name = "photo"

    async def download_min_size(
        self, *, session: typing.Optional[aiohttp.ClientSession] = None
    ) -> bytes:
        return await download_file(
            self.fields["sizes"][0]["url"], session=session
        )

    async def download_with_size(
        self,
        size: str,
        *,
        session: typing.Optional[aiohttp.ClientSession] = None,
    ) -> bytes:
        for photo_size in self.fields["sizes"]:
            if photo_size["type"] == size:
                return await download_file(photo_size["url"], session=session)
        raise ValueError(f"There isn’t a size `{size}` in available sizes")

    async def download_max_size(
        self, *, session: typing.Optional[aiohttp.ClientSession] = None
    ) -> bytes:
        return await download_file(
            self.fields["sizes"][-1]["url"], session=session
        )


class Document(Attachment):
    _name = "doc"
