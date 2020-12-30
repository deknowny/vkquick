from __future__ import annotations

import io

from vkquick.base.serializable import Attachment
from vkquick.utils import download_file


class Photo(Attachment):
    _name = "photo"

    async def download_min_size(self) -> bytes:
        return await download_file(self.fields.sizes[-1].url)

    async def download_with_size(self, size: chr) -> bytes:
        for photo_size in self.fields.sizes:
            if photo_size.type == size:
                return await download_file(photo_size.url)
        raise ValueError(f"There isn’t a size `{size}`")

    async def download_max_size(self):
        return await download_file(self.fields.sizes[0].url)


class Document(Attachment):
    _name = "doc"
