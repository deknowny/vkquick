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
import urllib.parse
import urllib.request
import typing as ty

import attrdict
import orjson

import vkquick.exceptions
import vkquick.request


class TokenOwner(str, enum.Enum):
    """
    Тип владельца токена. Используется
    для определения задержки между API запросами
    """

    GROUP = "group"
    USER = "user"


@dataclasses.dataclass
class API:
    """
    Обработчик всех API запросов

    Later
    """

    token: str
    """
    Access token для API запросов
    """

    version: ty.Union[float, str] = "5.133"
    """
    Версия API
    """

    autocomplete_params: ty.Dict[str, ty.Any] = dataclasses.field(default_factory=dict)
    """
    При вызове API метода первым аргументом можно передать Ellipsis,
    тогда в вызов метода подставятся поля из этого аргумента 
    """

    host: str = "api.vk.com"
    """
    URL отправки API запросов
    """

    response_factory: ty.Callable[[dict], ty.Any] = attrdict.AttrMap
    """
    Обертка для ответов (по умолчанию -- `attrdict.AttrMap`,
    чтобы иметь возможность получать поля ответа через точку)
    """

    def __post_init__(self):
        self._method_name = ""
        self._last_request_time = 0
        self.token_owner = self.define_token_owner(self.token, self.version)
        self._delay = 1 / 3 if self.token_owner == TokenOwner.USER else 1 / 20
        self.requests_session = vkquick.request.RequestsSession(host=self.host)

    def __getattr__(self, attribute) -> API:
        """
        Выстраивает имя метода путем переложения
        имен API методов на "получение атрибутов".

        Например

            await API(...).messages.send(...)

        Вызовет API метод `messages.send`. Также есть
        поддержка конвертации snake_case в camelCase:

            await API(...).messages.get_conversations_by_id(...)

        Что вызовет метод `messages.getConversationsById`
        """
        attribute = self._convert_name(attribute)
        if self._method_name:
            self._method_name += f".{attribute}"
        else:
            self._method_name = attribute
        return self

    def __call__(self, use_autocomplete_params_: bool = False, /, **request_params):
        """
        Вызывает API метод с полями из
        `**request_params` и именем метода, полученным через __getattr__

        При `attach_group_id_` добавит параметр `group_id` в запрос
        """
        method_name = self._convert_name(self._method_name)
        request_params = self._fill_request_params(request_params)
        if use_autocomplete_params_:
            request_params.update(self.autocomplete_params)
        self._method_name = str()
        return self._make_api_request(
            method_name=method_name, request_params=request_params
        )

    def method(
        self, method_name: str, request_params: ty.Dict[str, ty.Any], /
    ):
        """
        Делает API запрос аналогчино `__call__`,
        но при этом передавая метод строкой
        """
        method_name = self._convert_name(method_name)
        # Добавление пользовтельских параметров
        # запроса к токену и версии. Сделано не через
        # `request_params.update` для возможности перекрытия
        # параметрами пользователя
        request_params = self._fill_request_params(request_params)
        return self._make_api_request(
            method_name=method_name, request_params=request_params
        )

    async def _make_api_request(
        self, method_name: str, request_params: ty.Dict[str, ty.Any]
    ) -> ty.Union[API.response_factory, ty.Any]:
        """
        Создание API запросов путем передачи имени API и параметров
        """
        # API вк не умеет в массивы, поэтому все перечисления
        # Нужно отправлять строкой с запятой как разделителем
        for key, value in request_params.items():
            if isinstance(value, (list, set, tuple)):
                request_params[key] = ",".join(map(str, value))

        data = urllib.parse.urlencode(request_params)
        await self._waiting()
        query = (
            f"GET /method/{method_name}?{data} HTTP/1.1\n"
            f"Host: {self.host}\n\n"
        )
        await self.requests_session.write(query.encode("UTF-8"))
        body = await self.requests_session.read_body()
        body = orjson.loads(body)
        self._check_errors(body)
        if isinstance(body["response"], dict):
            return self.response_factory(body["response"])
        return body["response"]

    def _fill_request_params(self, params: ty.Dict[str, ty.Any]):
        """
        Добавляет к параметрам токен и версию API.
        Дефолтный `access_token` и `v` могут быть перекрыты
        """

        return {
            "access_token": self.token,
            "v": self.version,
            **params,
        }

    @staticmethod
    def _upper_zero_group(match: ty.Match) -> str:
        """
        Поднимает все символы в верхний
        регистр у captured-группы `let`. Используется
        для конвертации snake_case в camelCase
        """
        return match.group("let").upper()

    def _convert_name(self, name: str) -> str:
        """
        Конвертирует snake_case в camelCase
        """
        return re.sub(r"_(?P<let>[a-z])", self._upper_zero_group, name)

    @staticmethod
    def _check_errors(response: ty.Dict[str, ty.Any]) -> None:
        """
        Проверяет, является ли ответ от вк ошибкой
        """
        if "error" in response:
            raise vkquick.exceptions.VkApiError.destruct_response(response)

    @staticmethod
    def define_token_owner(token: str, version: str = "5.133"):
        attached_query = urllib.parse.urlencode(
            {"access_token": token, "v": version}
        )
        resp = urllib.request.urlopen(
            f"https://api.vk.com/method/users.get?{attached_query}",
            context=ssl.SSLContext(),
        )
        resp = orjson.loads(resp.read())
        return TokenOwner.USER if resp["response"] else TokenOwner.GROUP

    async def _waiting(self) -> None:
        """
        Ожидание после последнего API запроса
        (длительность в зависимости от владельца токена:
        1/20 для групп и 1/3  для пользователей).
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
