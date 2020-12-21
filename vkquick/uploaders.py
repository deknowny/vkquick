import json
import typing as ty

import aiohttp

from vkquick.api import API
from vkquick.wrappers.photo import Photo


async def upload_photos_to_message(*photos: ty.Union[bytes, str], api: API, peer_id: int = 0) -> ty.List[Photo]:
    if not (0 < len(photos) < 11):
        raise ValueError("You can attach from 1 to 10 photos")
    data = aiohttp.FormData()
    for ind, photo in enumerate(photos, 1):
        if isinstance(photo, str):
            real_photo = open(photo, "rb").read()
        else:
            real_photo = photo
        data.add_field(
            f"file{ind}", real_photo,
            content_type="multipart/form-data",
            filename=f"a.png"  # Расширение не играет роли, но без него не работает
        )

    upload_info = await api.photos.get_messages_upload_server(
        peer_id=peer_id
    )
    async with api.async_http_session.post(upload_info.upload_url, data=data) as response:
        # Нельзя .json() из-за некорректного хедера text/html, хотя там application/json
        response = await response.read()
        response = json.loads(response)

    photos = await api.photos.save_messages_photo(**response)
    photos = [Photo(photo) for photo in photos]
    return photos


async def upload_photo_to_message(photo: ty.Union[bytes, str], api: API, peer_id: int = 0) -> Photo:
    photos = await upload_photos_to_message(photo, api=api, peer_id=peer_id)
    return photos[0]
