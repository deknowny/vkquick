"""
Управление API запросами
"""
from __future__ import annotations
import asyncio
import dataclasses
import enum
import re
import ssl
import time
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Union


import aiohttp
import attrdict

from . import exception


class TokenOwner(enum.Enum):
    """
    Тип владельца токена. Используется
    для определения задержки между API запросами
    """

    GROUP = enum.auto()
    USER = enum.auto()


@dataclasses.dataclass
class API:

    token: str
    version: Union[float, str] = "5.124"
    owner: TokenOwner = TokenOwner.USER
    group_id: Optional[int] = None
    URL: str = "https://api.vk.com/method/"
    response_factory: Callable[[dict], Any] = attrdict.AttrMap

    def __post_init__(self):
        self._method_name = ""
        self._last_request_time = 0
        self._delay = 1 / 3 if self.owner == TokenOwner.USER else 1 / 20

    def __getattr__(self, attribute) -> "API":
        """
        Выстраивает имя метода путем переложения
        имен API методов на "получение атрибутов".

        Например

            API(...).messages.send(...)

        Вызовет API метод `messages.send`. Также есть
        поддержка конвертации snake_case в camelCaseself:

            API(...).messages.get_conversations_by_id(...)

        Что вызовет метод `messages.getConversationsById`
        """
        attribute = self._convert_name(attribute)
        if self._method_name:
            self._method_name += f".{attribute}"
        else:
            self._method_name = attribute
        return self

    def __call__(self, **request_params):
        """
        Вызывает API метод с полями из
        **kwargs и именем метода, полученным через __getattr__
        """
        method_name = self._convert_name(self._method_name)
        request_params = self._fill_request_params(request_params)
        self._method_name = str()
        return self._make_api_request(
            method_name=method_name, request_params=request_params
        )

    def method(self, method_name: str, request_params: Dict[str, Any], /):
        """
        Делает API запрос аналогчино `__call__`,
        но при этом передавая метод строкой
        """
        method_name = self._convert_name(name)
        # Добавление пользовтельских параметров
        # запроса к токену и версии. Сделано не через
        # `request_params.update` для возможности перекрытия
        # параметрами пользователя
        request_params = self._fill_request_params(request_params)
        return self._make_api_request(
            method_name=method_name, request_params=request_params
        )

    async def _make_api_request(
        self, method_name: str, request_params: Dict[str, Any]
    ) -> Union[API.response_factory, str, int]:
        """
        Создание API запросов путем передачи имени API и параметров
        """
        await self._waiting()
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=f"{self.URL}{method_name}",  # f-string быстрее
                data=request_params,
                ssl=ssl.SSLContext(),
            ) as response:
                response = await response.json()
                self._check_errors(response)
                if isinstance(response["response"], dict):
                    return self.response_factory(response["response"])
                return response["response"]

    def _fill_request_params(self, params: Dict[str, Any]):
        """
        Добавляет к параметрам токен и версию API
        """
        return {
            "access_token": self.token,
            "v": self.version,
            **params,
        }

    @staticmethod
    def _upper_zero_group(match: re.Match) -> str:
        """
        Поднимает все символы в верхний
        регистр у captured-группы `let`. Используется
        для конвертации snake_case в camelCase
        """
        return match.group("let").upper()

    def _convert_name(self, name: str) -> str:
        """
        Конвертирует snake_case to camelCase
        """
        return re.sub(r"_(?P<let>[a-z])", self._upper_zero_group, name)

    def _check_errors(self, response: Dict[str, Any]) -> None:
        """
        Проверяет, является ли ответ от вк ошибкой
        """
        if "error" in response:
            raise exception.VkApiError.destruct_response(response)

    async def _waiting(self) -> None:
        """
        Ожидание после последнего API запроса
        (длительность в зависимости от владельца токена:
        1/20 для групп и 1/43  для пользователей).
        Без этой задержки вк вернет ошибку о
        слишком частом обращении к API
        """
        now = time.time()
        diff = now - self._last_request_time
        if diff < self._delay:
            wait_time = self._delay - diff
            self._last_request_time += self._delay
            await asyncio.sleep(wait_time)
        else:
            self._last_request_time = now
