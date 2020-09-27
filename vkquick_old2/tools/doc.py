from pathlib import Path
from io import TextIOWrapper, BytesIO
from dataclasses import dataclass
from functools import partial, wraps
from typing import Union, Literal
import asyncio
import concurrent.futures

import attrdict

# But it's async via concurrent.futures.ThreadPoolExecutor()
import requests

from .uploader import Uploader
from vkquick import current


@dataclass
class _DocGetter:
    """
    Загрузчик и ~~сохранятор~~ документов
    """

    data_upload: dict
    method_save: str
    method_upload: str
    files: dict

    async def __call__(self, **kwargs):
        """
        Передайте сюда аргументы для ```save``` метода
        """
        resp = await current.api.method(self.method_upload, self.data_upload)
        loop = asyncio.get_running_loop()

        with concurrent.futures.ThreadPoolExecutor() as pool:
            resp = await loop.run_in_executor(
                pool,
                partial(
                    requests.post, url=resp["upload_url"], files=self.files
                ),
            )
        resp = resp.json()
        resp.update(kwargs)
        data = await current.api.method(self.method_save, resp)
        data = Doc(data)

        return data


class Doc(Uploader):
    """
    Загрузчик документов. После загрузки возвращает
    инстанс себя с полем `info`, которое содержит
    все поля объекта документа VK.
    Вы также можете создать инстанс по объекту документа,
    полученного другим образом (например, из attachments события).
    Объект автоматически конвертируется в нужное значение при передачи в `vq.Message`.

    ## Поля быстрого доступа (помимо `info`):
    * `full_id`:
    Совмещение `owner_id` и ID самого документа. Например:
    `-34534_223453413`
    * `as_attach`:
    "doc" + `full_id`. Если есть параметр
    `access_key` -- он также добавится.
    Например: `doc-34534_223453413_ab52364ce86`
    """

    def __init__(self, info: dict):
        self.info = attrdict.AttrMap(info)
        data = attrdict.AttrMap(self.info[self.info.type])
        self.full_id = f"{data.owner_id}_{data.id}"
        self.as_attach = f"doc{self.full_id}"
        if "access_key" in self.info:
            self.as_attach += f"_{data.access_key}"

    def __repr__(self):
        return self.as_attach

    def _uploader(method_upload, method_save):
        def wrapper(func):
            @wraps(func)
            def inside(*args, **kwargs):
                data_save, files = func(*args, **kwargs)
                return _DocGetter(
                    data_upload=data_save,
                    method_save=f"docs.{method_save}",
                    method_upload=f"docs.{method_upload}",
                    files=files,
                )

            return inside

        return wrapper

    @staticmethod
    def _get_file(data):
        """
        Получает байты из переданного объекта под файл
        """
        if isinstance(data, TextIOWrapper) or isinstance(data, BytesIO):
            return data.read()
        elif isinstance(data, Path):
            with open(data, "rb") as file:
                return file.read()
        elif isinstance(data, bytes) or isinstance(data, str):
            return data
        else:
            raise ValueError("Invalid data format")

    @staticmethod
    @_uploader("get_messages_upload_server", "save")
    def message(
        file: Union[str, bytes, TextIOWrapper, BytesIO, Path],
        type_: Literal["doc", "audio_message", "graffiti"],
        peer_id: int,
    ):
        """
        Загружает документ для отправки в сообщение
        """
        return (
            {"peer_id": peer_id, "type": type_},
            {
                "file": (
                    "file.txt",
                    Doc._get_file(file),
                    "multipart/form-data",
                )
            },
        )

    @staticmethod
    @_uploader("get_wall_upload_server", "save")
    def wall(
        file: Union[str, bytes, TextIOWrapper, BytesIO, Path], group_id: int
    ):
        """
        Загружает документ для поста
        """
        return (
            {"group_id": group_id},
            {
                "file": (
                    "file.txt",
                    Doc._get_file(file),
                    "multipart/form-data",
                )
            },
        )
