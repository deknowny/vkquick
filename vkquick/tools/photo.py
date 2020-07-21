from typing import Union
from typing import Optional
from pathlib import Path
from functools import wraps, partial
from dataclasses import dataclass
import io
import ssl
import asyncio
import concurrent.futures

import requests
import aiohttp
import attrdict

from vkquick import current
from .uploader import Uploader


@dataclass
class _PhotosGetter:
    """
    ~Сохранятор~ и загрузчик фотографий
    """

    data_upload: dict
    method_save: str
    method_upload: str
    files: dict

    async def __call__(self, **kwargs):
        """
        Передайте сюда параметры для ```save``` метода
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
        data = [Photo(i) for i in data]

        return data


class Photo(Uploader):
    """
    Загрузчик фотографий.
    Каждая переданная фотография в тот
    или иной _статический загрузчик_ представляет собой один из следующих объектов:

    * bytes / BytesIO
    * pathlib.Path либо строка. В обоих случая фотография будет получена из файлов

    Вы можете загрузить фотографию по ссылке методом `Photo.download`,
    тем самым получить ее байты и передать их в один из загрузчиков

    Каждый загрузчик, после которого был вызван
    <del>сохранятор</del> обработчик сохранений и загрузки
    (просто еще одни скобочки), вернет инстанс этого класса со следующими полями:

    * ```info```:
    Все содержимое объекта документа
    * ```full_id```:
    ID владельца + ID документа. Например, ```3245345_3453453453```
    * ```as_attach```:
    Строка, которую можно использовать в
    attachment. Если поле ```access_key```
    присутствует в объекте, оно также добавится в конец.
    Например, ```photo3245345_3453453453_a6be678d23a```

    ## Пример
    1. Находит фотографии в файлах и загружает
    их для отправки в сообщении в ответ на команду ```/send photo```

            import vkquick as vq


            @vq.Cmd(names=["send photo"], prefs=["/"])
            @vq.Reaction("message_new")
            async def send_photo(event: vq.Event):
                photos = vq.Photo.message(
                    "example123.png",
                    "example456.png",
                    peer_id=event.object.message.peer_id
                )
                photos = await photos() # Сюда можно передать параметры для messages.saveMessagesPhoto

                return vq.Message("Your photo:", attachment=photos)

    1. Загружает фотографии переданным ссылкам и отправляет их


            import vkquick as vq


            @vq.Cmd(names=["download"], prefs=["/"])
            @vq.Reaction("message_new")
            async def send_photo_by_url(
                urls: [vq.Word],
                event: vq.Event
            ):
                photos = [
                    await vq.Photo.download(url)
                    for url in urls
                ]
                photos = vq.Photo.message(
                    *photos,
                    peer_id=event.object.message.peer_id
                )

                photos = await photos()

                return vq.Message("Downloaded photos:", attachment=photos)


    """

    def __init__(self, info: dict):
        self.info = attrdict.AttrMap(info)
        self.full_id = f"{self.info.owner_id}_{self.info.id}"
        self.as_attach = f"photo{self.full_id}"
        if "access_key" in self.info:
            self.as_attach += f"_{self.info.access_key}"

    def __repr__(self):
        return self.as_attach

    @staticmethod
    async def download(url):
        """
        Скачивает фотографию и возвращает ее байты по ссылке ```url```
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, ssl=ssl.SSLContext()) as resp:
                return await resp.read()

    def _uploader(method_upload, method_save):
        def wrapper(func):
            @wraps(func)
            def inside(*args, **kwargs):
                data_save, files = func(*args, **kwargs)
                return _PhotosGetter(
                    data_upload=data_save,
                    method_save=f"photos.{method_save}",
                    method_upload=f"photos.{method_upload}",
                    files=files,
                )

            return inside

        return wrapper

    @staticmethod
    def _get_photo(data):
        if isinstance(data, io.BytesIO):
            return data.read()
        elif isinstance(data, Path) or isinstance(data, str):
            with open(data, "rb") as file:
                return file.read()
        elif isinstance(data, bytes):
            return data
        elif data is None:
            return None

        else:
            raise ValueError("Invalid data format")

    @staticmethod
    @_uploader("get_upload_server", "save")
    def album(
        file1: Union[str, bytes, Path],
        file2: Optional[Union[str, bytes, Path]] = None,
        file3: Optional[Union[str, bytes, Path]] = None,
        file4: Optional[Union[str, bytes, Path]] = None,
        file5: Optional[Union[str, bytes, Path]] = None,
        album_id: Optional[int] = None,
        group_id: Optional[int] = None,
    ):
        """
        Загружает фотографии в альбом
        """
        files = {
            "file1": (
                "file.png",
                Photo._get_photo(file1),
                "multipart/form-data",
            ),
            "file2": (
                "file.png",
                Photo._get_photo(file2),
                "multipart/form-data",
            ),
            "file3": (
                "file.png",
                Photo._get_photo(file3),
                "multipart/form-data",
            ),
            "file4": (
                "file.png",
                Photo._get_photo(file4),
                "multipart/form-data",
            ),
            "file5": (
                "file.png",
                Photo._get_photo(file5),
                "multipart/form-data",
            ),
        }
        files = filter(lambda x: x[1] is not None, files.items())
        files = dict(files)
        data = dict(album_id=album_id, group_id=group_id)

        return data, files

    @staticmethod
    @_uploader("get_wall_upload_server", "save_wall_photo")
    def wall(photo: Union[str, bytes, Path], group_id: Optional[int] = None):
        """
        Загружает фотографию на стену
        """
        return (
            {"group_id": group_id},
            {
                "file": (
                    "file.png",
                    Photo._get_photo(photo),
                    "multipart/form-data",
                )
            },
        )

    @staticmethod
    @_uploader("get_owner_photo_upload_server", "save_owner_photo")
    def page_ava(
        photo: Union[str, bytes, Path], owner_id: Optional[int] = None
    ):
        """
        Загружает фотографию на аватар пользователя/сообщества
        """
        return (
            {"owner_id": owner_id},
            {
                "photo": (
                    "file.png",
                    Photo._get_photo(photo),
                    "multipart/form-data",
                )
            },
        )

    @staticmethod
    @_uploader("get_messages_upload_server", "save_messages_photo")
    def message(*files: Union[str, bytes, Path], peer_id: int):
        """
        Загружает фотографии для отправки в сообщение
        """
        files = {
            f"file{ind}": (
                "file.png",
                Photo._get_photo(val),
                "multipart/form-data",
            )
            for ind, val in enumerate(files[:10])
        }

        return {"peer_id": peer_id}, files

    @staticmethod
    @_uploader("get_chat_upload_server", "set_chat_photo")
    def chat_ava(
        file: Union[str, bytes, Path],
        chat_id: int,
        crop_x: Optional[int],
        crop_y: Optional[int],
        crop_width: Optional[int],
    ):
        """
        Загружает фотографию на аватар чата
        """
        return (
            {
                "chat_id": chat_id,
                "crop_x": crop_x,
                "crop_y": crop_y,
                "crop_width": crop_width,
            },
            {"file": Photo._get_photo(file)},
        )

    @classmethod
    @_uploader("get_market_upload_server", "save_market_photo")
    def market(
        cls,
        file: Union[str, bytes, Path],
        group_id: int,
        main_photo: bool,
        crop_x: Optional[int],
        crop_y: Optional[int],
        crop_width: Optional[int],
    ):
        """
        Загружает фотографию товара
        """
        return (
            {
                "group_id": group_id,
                "crop_x": crop_x,
                "crop_y": crop_y,
                "crop_width": crop_width,
                "main_photo": main_photo,
            },
            {
                "file": (
                    "file.png",
                    cls._get_photo(file),
                    "multipart/form-data",
                )
            },
        )

    @staticmethod
    @_uploader("get_market_album_upload_server", "save_market_album_photo")
    def market_album(file: Union[str, bytes, Path], group_id: int):
        """
        Загружает фотографию в альбом товара
        """
        return (
            {"group_id": group_id},
            {
                "file": (
                    "file.png",
                    Photo._get_photo(file),
                    "multipart/form-data",
                )
            },
        )
