from __future__ import annotations

import asyncio
import enum
import os
import re
import time
import typing as ty
import urllib.parse

import aiohttp
import cachetools
from loguru import logger

from vkquick.base.api_serializable import APISerializableMixin
from vkquick.base.session_container import SessionContainerMixin
from vkquick.exceptions import VKAPIError
from vkquick.json_parsers import json_parser_policy
from vkquick.pretty_view import pretty_view

if ty.TYPE_CHECKING:
    from vkquick.base.json_parser import BaseJSONParser


@enum.unique
class TokenOwner(enum.Enum):
    """
    Тип владельца токена: пользователь/группа/не определено
    """
    USER = enum.auto()
    GROUP = enum.auto()
    UNKNOWN = enum.auto()


class API(SessionContainerMixin):
    """
    Основной класс, позволяющий с помощью токена выполнять API-запросы
    """
    def __init__(
        self,
        token: str,
        token_owner: TokenOwner = TokenOwner.UNKNOWN,
        version: str = "5.135",
        requests_url: str = "https://api.vk.com/method/",
        requests_session: ty.Optional[aiohttp.ClientSession] = None,
        json_parser: ty.Optional[BaseJSONParser] = None,
        cache_table: ty.Optional[cachetools.Cache] = None,
    ):
        SessionContainerMixin.__init__(
            self, requests_session=requests_session, json_parser=json_parser
        )
        if token.startswith("$"):
            self._token = os.environ[token[1:]]
        else:
            self._token = token
        self._version = version
        self._token_owner = token_owner
        self._requests_url = requests_url
        self._cache_table = cache_table or cachetools.TTLCache(
            ttl=3600, maxsize=2 ** 15
        )

        self._method_name = ""
        self._last_request_timestamp = 0.0
        self._use_cache = False
        self._stable_request_params = {
            "access_token": self._token,
            "v": self._version,
        }

        self._update_requests_delay()

    def use_cache(self) -> API:
        self._use_cache = True
        return self

    async def define_token_owner(self) -> TokenOwner:
        if self._token_owner != TokenOwner.UNKNOWN:
            return self._token_owner
        seemed_user = await self.use_cache().method("users.get")
        if seemed_user:
            self._token_owner = TokenOwner.USER
        else:
            self._token_owner = TokenOwner.GROUP

        self._update_requests_delay()
        return self._token_owner

    def _update_requests_delay(self) -> None:
        if self._token_owner in {TokenOwner.USER, TokenOwner.UNKNOWN}:
            self._requests_delay = 1 / 3
        else:
            self._requests_delay = 1 / 20

    def __getattr__(self, attribute: str) -> API:
        """
        Используя `__gettattr__`, класс предоставляет возможность
        вызывать методы API, как будто обращаясь к атрибутам.
        Пример есть в описании класса

        Arguments:
            attribute: Имя/заголовок названия метода
        Returns:
            Собственный инстанс класса для того,
            чтобы была возможность продолжить выстроить имя метода через точку
        """
        if self._method_name:
            self._method_name += f".{attribute}"
        else:
            self._method_name = attribute
        return self

    async def __call__(
        self,
        **request_params,
    ) -> ty.Any:
        """
        Выполняет необходимый API запрос с нужным методом и параметрами,
        добавляя к ним токен и версию (может быть перекрыто)

        Arguments:
            allow_cache: Если `True` -- результат запроса
                с подобными параметрами и методом будет получен из кэш-таблицы,
                если отсутствует -- просто занесен в таблицу. Если `False` -- запрос
                просто выполнится по сети
            request_params: Параметры, принимаемы методом, которые описаны в документации API

        Returns:
            Пришедший от API ответ
        """
        method_name = self._method_name
        self._method_name = ""
        return await self.method(method_name, **request_params)

    async def method(self, method_name: str, **request_params) -> ty.Any:
        """
        Выполняет необходимый API запрос с нужным методом и параметрами.

        Arguments:
            method_name: Имя вызываемого метода API
            request_params: Параметры, принимаемы методом, которые описаны в документации API.
            allow_cache: Если `True` -- результат запроса
                с подобными параметрами и методом будет получен из кэш-таблицы,
                если отсутствует -- просто занесен в таблицу. Если `False` -- запрос
                просто выполнится по сети.

        Returns:
            Пришедший от API ответ.

        Raises:
            VKAPIError: В случае ошибки, пришедшей от некорректного вызова запроса.
        """
        use_cache = self._use_cache
        self._use_cache = False
        return await self._make_api_request(
            method_name=method_name,
            request_params=request_params,
            use_cache=use_cache
        )

    async def execute(self, code: str, /) -> ty.Any:
        """
        Исполняет API метод `execute` с переданным VKScript-кодом.

        Arguments:
            code: VKScript код

        Returns:
            Пришедший ответ от API

        Raises:
            VKAPIError: В случае ошибки, пришедшей от некорректного вызова запроса.
        """
        return await self.method("execute", code=code)

    async def _make_api_request(
        self,
        method_name: str,
        request_params: ty.Dict[str, ty.Any],
        use_cache: bool
    ) -> ty.Any:
        """
        Выполняет API запрос на определнный метод с заданными параметрами

        Arguments:
            method_name: Имя метода API
            request_params: Параметры, переданные для метода
            allow_cache: Использовать кэширование

        Raises:
            VKAPIError: В случае ошибки, пришедшей от некорректного вызова запроса.
        """
        # Конвертация параметров запроса под особенности API и имени метода
        real_method_name = _convert_method_name(method_name)
        real_request_params = _convert_params_for_api(request_params)
        extra_request_params = self._stable_request_params.copy()
        extra_request_params.update(real_request_params)

        # Определение владельца токена нужно
        # для определения задержки между запросами
        if self._token_owner is None:
            await self.fetch_token_owner_entity()

        # Кэширование запросов по их методу и переданным параметрам
        # `cache_hash` -- ключ кэш-таблицы
        if use_cache:
            cache_hash = urllib.parse.urlencode(real_request_params)
            cache_hash = f"{method_name}#{cache_hash}"
            if cache_hash in self._cache_table:
                return self._cache_table[cache_hash]

        # Задержка между запросами необходима по правилам API
        api_request_delay = self._get_waiting_time()
        await asyncio.sleep(api_request_delay)

        # Отправка запроса с последующей проверкой ответа
        response = await self._send_api_request(
            real_method_name, extra_request_params
        )
        logger.opt(colors=True).info(
            "Called method <m>{method_name}</m>({method_params})".format(
                method_name=real_method_name,
                method_params=", ".join(
                    f"<c>{key}</c>=<y>{value!r}</y>"
                    for key, value in real_request_params.items()
                ),
            )
        )
        logger.opt(lazy=True).debug(
            "Response is: {response}", response=lambda: pretty_view(response)
        )

        if "error" in response:
            raise VKAPIError.destruct_response(response)
        else:
            response = response["response"]

        # Если кэширование включено -- запрос добавится в таблицу
        if use_cache:
            self._cache_table[cache_hash] = response
            self._use_cache = False

        return response

    async def _send_api_request(self, method_name: str, params: dict) -> dict:
        async with self.requests_session.post(
            self._requests_url + method_name, data=params
        ) as response:
            loaded_response = await self.parse_json_body(response)
            return loaded_response

    def _get_waiting_time(self) -> float:
        """
        Рассчитывает обязательное время задержки после
        последнего API запроса. Для групп -- 0.05s,
        для пользователей/сервисных токенов -- 0.333s

        Returns:
            Время, необходимое для ожидания.
        """
        now = time.time()
        diff = now - self._last_request_timestamp
        if diff < self._requests_delay:
            wait_time = self._requests_delay - diff
            self._last_request_timestamp += wait_time
            return wait_time
        else:
            self._last_request_timestamp = now
            return 0.0


def _convert_param_value(value, /):
    """
    Конвертирует параметер API запроса в соотвествиями
    с особенностями API и дополнительными удобствами

    Arguments:
        value: Текущее значение параметра

    Returns:
        Новое значение параметра

    """
    # Для всех перечислений функция вызывается рекурсивно.
    # Массивы в запросе распознаются вк только если записать их как строку,
    # перечисляя значения через запятую
    if isinstance(value, (list, set, tuple)):
        updated_sequence = map(_convert_param_value, value)
        return ",".join(updated_sequence)

    # Все словари, как списки, нужно сдампить в JSON
    elif isinstance(value, dict):
        return json_parser_policy.dumps(value)

    # Особенности `aiohttp`
    elif isinstance(value, bool):
        return int(value)

    # Если класс определяет протокол сериализации под параметр API,
    # используется соотвествующий метод
    elif isinstance(value, APISerializableMixin):
        new_value = value.represent_as_api_param()
        return _convert_param_value(new_value)

    # Для корректного отображения в логах
    elif isinstance(value, int):
        return value

    else:
        return str(value)


def _convert_params_for_api(params: dict, /):
    """
    Конвертирует словарь из параметров для метода API,
    учитывая определенные особенности

    Arguments:
        params: Параметры, передаваемые для вызова метода API

    Returns:
        Новые параметры, которые можно передать
        в запрос и получить ожидаемый результат

    """
    updated_params = {
        (key[:-1] if key.endswith("_") else key): _convert_param_value(value)
        for key, value in params.items()
        if value is not None
    }
    return updated_params


def _upper_zero_group(match: ty.Match, /) -> str:
    """
    Поднимает все символы в верхний
    регистр у captured-группы `let`. Используется
    для конвертации snake_case в camelCase.

    Arguments:
      match: Регекс-группа, полученная в результате `re.sub`

    Returns:
        Ту же букву из группы, но в верхнем регистре

    """
    return match.group("let").upper()


def _convert_method_name(name: str, /) -> str:
    """
    Конвертирует snake_case в camelCase.

    Arguments:
      name: Имя метода, который необходимо перевести в camelCase

    Returns:
        Новое имя метода в camelCase

    """
    return re.sub(r"_(?P<let>[a-z])", _upper_zero_group, name)
