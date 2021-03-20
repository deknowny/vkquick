from __future__ import annotations

from vkquick.base.serializable import Attachment
from vkquick.utils import download_file


class Photo(Attachment):
    _name = "photo"

    async def download_min_size(self) -> bytes:
        return await download_file(self.fields.sizes[0].url)

    async def download_with_size(self, size: str) -> bytes:
        for photo_size in self.fields.sizes:
            if photo_size.type == size:
                return await download_file(photo_size.url)
        raise ValueError(f"There isn’t a size `{size}` in available sizes")

    async def download_max_size(self) -> bytes:
        return await download_file(self.fields.sizes[-1].url)


class Document(Attachment):
    _name = "doc"
