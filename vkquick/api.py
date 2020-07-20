"""
Управление API запросами
"""
import asyncio
import ssl
import time
import re
from typing import Dict
from typing import Any
from typing import Optional
from typing import Literal
from dataclasses import dataclass

import aiohttp
import attrdict
import colorama

from . import exception as ex
from .annotypes.base import Annotype
from . import current


colorama.init()


@dataclass
class API(Annotype):
    """
    Отправляет запросы к API

    Поддерживает конвертацию snake_case
    в camelCase в именах у методов
    """

    token: str
    """
    Токен пользователя или группы
    """
    version: float
    """
    Верия API
    """
    owner: Literal["group", "user"]
    """
    Тип обладателя токена
    """
    group_id: Optional[int] = None
    """
    Передавайте, только если нужен аргумент ```as_group_```
    """
    URL: str = "https://api.vk.com/method/"
    """
    URL API запросов
    """
    factory: type = attrdict.AttrMap
    """
    Фабрика для возвращаемых ответов
    """

    def __post_init__(self):
        self._method = ""
        self._last_request_time = 0
        self._delay = 1 / 20 if self.owner == "group" else 1 / 3

    def __getattr__(self, attr) -> "API":
        """
        Выстраивает имя метода
        """
        attr = self._convert_name(attr)
        if self._method:
            self._method += f".{attr}"
        else:
            self._method = attr
        return self

    def __call__(self, as_group_: bool = False, /, **kwargs):
        """
        Вызывает метод с полями из
        **kwargs. При as_group_=True
        автоматически добавится поле
        group_id=<id группы>.
        Сделано для обращений к методами
        группы от лица пользователя
        """
        if as_group_:
            kwargs.update(group_id=self.group_id)
        meth_name = self._method
        self._method = str()
        result = self.method(name=meth_name, data=kwargs)
        return result

    @staticmethod
    def prepare(argname, event, func, bin_stack):
        return current.api

    async def method(self, name: str, data: dict):
        """
        Вызовает API метод с
        именем меотда из параметра
        ```name``` и полями из ```data```
        """
        name = self._convert_name(name)
        await self._waiting()
        data = {"access_token": self.token, "v": self.version, **data}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=self.URL + name, data=data, ssl=ssl.SSLContext()
            ) as response:
                response = await response.json()
                self._check_errors(response)
                if isinstance(response["response"], dict):
                    return self.factory(response["response"])
                return response["response"]

    @staticmethod
    def _upper_zero_group(match):
        return match.group("let").upper()

    def _convert_name(self, name):
        """
        Convert snake_case to camelCase
        """
        return re.sub(r"_(?P<let>[a-z])", self._upper_zero_group, name)

    def _check_errors(self, resp: Dict[str, Any]) -> None:
        if "error" in resp:
            raise ex.VkErr(ex.VkErrPreparing(resp))

    async def _waiting(self):
        """
        Waiting before the last API requst 0.05 or 1/3
        seconds. Without this you'll capture the API error
        so it protects you
        """
        now = time.time()
        diff = now - self._last_request_time
        if diff < self._delay:
            wait_time = self._delay - diff
            self._last_request_time += self._delay
            await asyncio.sleep(wait_time)
        else:
            self._last_request_time = now
