import json
import pathlib
import typing as ty

import aiohttp

from vkquick.api import API
from vkquick.wrappers.attachment import Photo, Document


async def upload_photos_to_message(
    *photos: ty.Union[bytes, str], api: API, peer_id: int = 0
) -> ty.List[Photo]:
    if not (0 < len(photos) < 11):
        raise ValueError("You can attach from 1 to 10 photos")
    data = aiohttp.FormData()
    for ind, photo in enumerate(photos, 1):
        if isinstance(photo, str):
            real_photo = open(photo, "rb").read()
        else:
            real_photo = photo
        data.add_field(
            f"file{ind}",
            real_photo,
            content_type="multipart/form-data",
            filename=f"a.png",  # Расширение не играет роли, но без него не работает
        )

    upload_info = await api.photos.get_messages_upload_server(peer_id=peer_id)
    async with api.async_http_session.post(
        upload_info.upload_url, data=data
    ) as response:
        # Нельзя .json() из-за некорректного хедера text/html, хотя там application/json
        response = await response.read()
        response = json.loads(response)

    photos = await api.photos.save_messages_photo(**response)
    photos = [Photo(photo) for photo in photos]
    return photos


async def upload_photo_to_message(
    photo: ty.Union[bytes, str], api: API, peer_id: int = 0
) -> Photo:
    photos = await upload_photos_to_message(photo, api=api, peer_id=peer_id)
    return photos[0]


@ty.overload
async def upload_doc_to_message(
    *,
    content: ty.Union[str, bytes],
    filename: str,
    api: API,
    peer_id: int,
    tags: ty.Optional[str] = None,
    return_tags: ty.Optional[bool] = None,
    type_: ty.Optional[ty.Literal["doc", "audio_message", "graffiti"]] = None,
) -> Document:
    pass


@ty.overload
async def upload_doc_to_message(
    *,
    filepath: str,
    api: API,
    peer_id: int,
    filename: ty.Optional[str] = None,
    tags: ty.Optional[str] = None,
    return_tags: ty.Optional[bool] = None,
    type_: ty.Optional[ty.Literal["doc", "audio_message", "graffiti"]] = None,
) -> Document:
    pass


async def upload_doc_to_message(
    *,
    api: ty.Optional[API],
    peer_id: ty.Optional[int],
    content: ty.Optional[ty.Union[str, bytes]] = None,
    filename: ty.Optional[str] = None,
    filepath: ty.Optional[str] = None,
    tags: ty.Optional[str] = None,
    return_tags: ty.Optional[bool] = None,
    type_: ty.Optional[ty.Literal["doc", "audio_message", "graffiti"]] = None,
) -> Document:

    if content is not None and filename is not None and filepath is not None:
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
    async with api.async_http_session.post(
        upload_info.upload_url, data=data
    ) as response:
        response = await response.read()
        response = json.loads(response)
    doc = await api.docs.save(
        **response, title=filename, tags=tags, return_tags=return_tags
    )
    doc = Document(doc[type_ or "doc"])
    return doc
