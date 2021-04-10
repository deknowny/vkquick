from __future__ import annotations

import pathlib
import typing as ty

import aiohttp
import typing_extensions as tye

from vkquick import API
from vkquick.ext.chatbot.utils import download_file
from vkquick.ext.chatbot.providers.base import Provider
from vkquick.ext.chatbot.wrappers.attachment import Photo, Document


class PhotoProvider(Provider[Photo]):
    @classmethod
    async def upload_many_to_message(
        cls, *photos: ty.Union[bytes, str], api: API, peer_id: int = 0
    ) -> ty.List[PhotoProvider]:
        if not (0 < len(photos) < 6):
            raise ValueError("You can upload only from 1 to 5 photos")
        data = aiohttp.FormData()
        for ind, photo in enumerate(photos):
            if isinstance(photo, str):
                real_photo = open(photo, "rb").read()
            else:
                real_photo = photo
            data.add_field(
                f"file{ind}",
                real_photo,
                content_type="multipart/form-data",
                filename=f"a.png",  # Расширение не играет роли
            )

        upload_info = await api.photos.get_messages_upload_server(
            peer_id=peer_id
        )
        async with api.requests_session.post(
            upload_info["upload_url"], data=data
        ) as response:
            response = await api.parse_json_body(response, content_type=None)

        photos = await api.photos.save_messages_photo(**response)
        photos = [
            PhotoProvider.from_mapping(api=api, storage=photo)
            for photo in photos
        ]
        return photos

    @classmethod
    async def upload_one_to_message(
        cls, photo: ty.Union[bytes, str], api: API, peer_id: int = 0
    ) -> PhotoProvider:
        photos = await cls.upload_many_to_message(
            photo, api=api, peer_id=peer_id
        )
        return photos[0]

    async def download_min_size(
        self, *, session: ty.Optional[aiohttp.ClientSession] = None
    ) -> bytes:
        return await download_file(
            self.storage["sizes"][0]["url"],
            session=session or self._api.requests_session,
        )

    async def download_with_size(
        self, size: str, *, session: ty.Optional[aiohttp.ClientSession] = None
    ) -> bytes:
        for photo_size in self.storage["sizes"]:
            if photo_size["type"] == size:
                return await download_file(
                    photo_size["url"],
                    session=session or self._api.requests_session,
                )
        raise ValueError(f"There isn’t a size `{size}` in available sizes")

    async def download_max_size(
        self, *, session: ty.Optional[aiohttp.ClientSession] = None
    ) -> bytes:
        return await download_file(
            self.storage["sizes"][-1]["url"],
            session=session or self._api.requests_session,
        )


class DocumentProvider(Provider[Document]):
    @classmethod
    @ty.overload
    async def upload_one_to_message(
        cls,
        *,
        content: ty.Union[str, bytes],
        filename: str,
        api: API,
        peer_id: int,
        tags: ty.Optional[str] = None,
        return_tags: ty.Optional[bool] = None,
        type_: ty.Optional[
            tye.Literal["doc", "audio_message", "graffiti"]
        ] = None,
    ) -> DocumentProvider:
        pass  # pragma: no cover

    @classmethod
    @ty.overload
    async def upload_one_to_message(
        cls,
        *,
        filepath: str,
        api: API,
        peer_id: int,
        filename: ty.Optional[str] = None,
        tags: ty.Optional[str] = None,
        return_tags: ty.Optional[bool] = None,
        type_: ty.Optional[
            tye.Literal["doc", "audio_message", "graffiti"]
        ] = None,
    ) -> DocumentProvider:
        pass  # pragma: no cover

    @classmethod
    async def upload_one_to_message(
        cls,
        *,
        api: ty.Optional[API],
        peer_id: ty.Optional[int],
        content: ty.Optional[ty.Union[str, bytes]] = None,
        filename: ty.Optional[str] = None,
        filepath: ty.Optional[str] = None,
        tags: ty.Optional[str] = None,
        return_tags: ty.Optional[bool] = None,
        type_: ty.Optional[
            tye.Literal["doc", "audio_message", "graffiti"]
        ] = None,
    ) -> DocumentProvider:

        if (
            content is not None
            and filename is not None
            and filepath is not None
        ):
            raise ValueError(
                "Can't upload 2 attachments. "
                "A file can be passed only via "
                "content and filename or only "
                "via filepath with optional filename, not both"
            )
        if filepath is not None:
            path = pathlib.Path(filepath)
            filename = path.name if filename is None else filename
            content = path.read_bytes()
        elif content is filename is None:
            raise ValueError(
                "Can't upload 2 attachments. "
                "A file can be passed only via "
                "content and filename or only "
                "via filepath"
            )
        data = aiohttp.FormData()
        data.add_field(
            f"file",
            content,
            content_type="multipart/form-data",
            filename=filename,
        )

        upload_info = await api.docs.get_messages_upload_server(
            peer_id=peer_id, type=type_
        )
        async with api.requests_session.post(
            upload_info["upload_url"], data=data
        ) as response:
            response = await api.parse_json_body(response, content_type=None)
        doc = await api.docs.save(
            **response, title=filename, tags=tags, return_tags=return_tags
        )
        doc = DocumentProvider.from_mapping(
            api=api, storage=doc[type_ or "doc"]
        )
        return doc
