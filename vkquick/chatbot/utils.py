import datetime
import random
import re
import ssl
import typing

import aiohttp

from vkquick.json_parsers import json_parser_policy


def random_id(side: int = 2 ** 31 - 1) -> int:
    """
    Случайное число в диапазоне +-`side`.
    Используется для API метода `messages.send`
    """
    return random.randint(-side, +side)


def peer(chat_id: int = 0) -> int:
    """
    Добавляет к `chat_id` значение, чтобы оно стало `peer_id`.
    Краткая и более приятная запись сложения любого числа с 2 000 000 000
    (да, на один символ)

    peer_id=vq.peer(123)
    """
    return 2_000_000_000 + chat_id


async def download_file(
    url: str,
    *,
    session: typing.Optional[aiohttp.ClientSession] = None,
    **kwargs,
) -> bytes:
    """
    Скачивание файлов по их прямой ссылке
    """
    used_session = session or aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=ssl.SSLContext()),
        skip_auto_headers={"User-Agent"},
        raise_for_status=True,
        json_serialize=json_parser_policy.dumps,
    )
    async with used_session.get(url, **kwargs) as response:
        downloaded_file = await response.read()

    if session is None:
        await used_session.close()

    return downloaded_file


_registration_date_regex = re.compile('ya:created dc:date="(?P<date>.*?)"')


async def get_user_registration_date(
    id_: int, *, session: typing.Optional[aiohttp.ClientSession] = None
) -> datetime.datetime:
    request_session = session or aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False),
        skip_auto_headers={"User-Agent"},
        raise_for_status=True,
        json_serialize=json_parser_policy.dumps,
    )
    async with request_session:
        async with request_session.get(
            "https://vk.com/foaf.php", params={"id": id_}
        ) as response:
            user_info = await response.text()
            registration_date = _registration_date_regex.search(user_info)
            if registration_date is None:
                raise ValueError(f"No such user with id `{id_}`")
            registration_date = registration_date.group("date")
            registration_date = datetime.datetime.fromisoformat(
                registration_date
            )
            return registration_date


def get_origin_typing(type):
    # If generic
    if typing.get_args(type):
        return typing.get_origin(type)
    return type
