"""
Управление API запросами

API ВКонтакте представляет собой набор
специальных "методов" для получения какой-либо информации.
Например, чтобы получить имя пользователя, нужно вызвать метод `users.get`
и передать в качестве параметра его ID.
Вызов метода и передача параметров представляет собой лишь отправку HTTP запроса.
Вызвать метод `some.method` и передать туда параметр `foo=1` означает составить
запрос такого вида: `https://api.vk.com/method/some.method?foo=1`.
Составлять такие запросы каждый раз достаточно неудобно, поэтому этот
модуль предоставляет возможности более комфортного взаимодействия

Список методов с параметрами можно найти на https://vk.com/dev/methods
"""
from __future__ import annotations

import asyncio
import dataclasses
import enum
import os
import json
import re
import time
import typing as ty
import urllib.parse

import aiohttp
import cachetools
import requests

from vkquick.base.serializable import APISerializable
from vkquick.base.aiohttp_session_container import AiohttpSessionContainer
from vkquick.events_generators.longpoll import GroupLongPoll, UserLongPoll, LongPollBase
from vkquick.exceptions import VKAPIError
from vkquick.json_parsers import json_parser_policy
from vkquick.wrappers.page_entity import User, Group, PageEntity


class API(AiohttpSessionContainer):
    """
    Этот класс предоставляет возможности удобного вызова API методов

        >>> import asyncio
        >>>
        >>> import vkquick as vq
        >>>
        >>>
        >>> async def main():
        >>>     api = vq.API("token")
        >>>
        >>>     # Вызов метода `users.get`
        >>>     durov = await api.users.get(user_ids=1)
        >>>     print(durov[0].first_name)  # Павел
        >>>
        >>>     # Альтернативный способ
        >>>     durov = await api.method("users.get", {"user_ids": 1})
        >>>     print(durov[0].first_name)  # Павел
        >>>
        >>>     # Кэширование
        >>>     # 1. Запрос, который закэшируется
        >>>     durov = await api.users.get(..., user_ids=1)
        >>>     # 2. Запрос, который уже не будет вызван.
        >>>     # Результат возьмется из кэша
        >>>     durov = await api.users.get(..., user_ids=1)
        >>>     print(durov[0].first_name)  # Павел
        >>>
        >>>     # Класс реализует некоторые API методы, добавляя к ним дополнительные обработки
        >>>     # Например, `fetch_user_via_id` -- кэшированное получение пользователя по его ID/`screen_name`,
        >>>     # который будет обернут в специальную обертку. Предпочтительнее, чем самостоятельный
        >>>     # вызов `users.get`. Все возможности обертки описаны в ней самой
        >>>     durov = await api.fetch_user_via_id(1)
        >>>     print(durov.fn)  # Павел
        >>>     print(f"Hi, {durov:<fn> <ln>}")  # Hi, Павел Дуров
        >>>     print(f"Hi, {durov:@<fn> <ln>}")  # Hi, [id1|Павел Дуров]
        >>>
        >>>     # По окончанию нужно закрыть сессию запросов (желательно в блоке try/finally).
        >>>     # Можно использовать асинхронный менеджер контекста
        >>>     await api.close_session()
        >>>
        >>>
        >>> asyncio.run(main())


    :param token: Токен пользователя/группы/сервисный для отправки API запросов.
        Можно использовать имя переменной окружения,
        если добавить в начало `"$"`, т.е. `"$ENV_VAR"`
    :param version: Версия используемого API.
    :param requests_url: URL для отправки запросов.
    :param requests_session: Собственная `aiohttp` сессия.
    """

    def __init__(
        self,
        token: str, *,
        version: ty.Union[float, str] = "5.135",
        requests_url: str = "https://api.vk.com/method/",
        requests_session: ty.Optional[aiohttp.ClientSession] = None
    ) -> None:
        super().__init__(requests_session)

        # Автоматическое получение токена из переменных окружения
        if token.startswith("$"):
            self._token = os.getenv(token[1:])
        else:
            self._token = token

        self._version = version
        self._requests_url = requests_url
        self._cache_table = cachetools.TTLCache(ttl=3600, maxsize=2 ** 15)

        self._method_name = ""
        self._last_request_stamp = 0
        self._requests_delay = 0
        self._token_owner = None
        self._stable_request_params = {
            "access_token": self._token,
            "v": self._version
        }

    def __getattr__(self, attribute: str) -> API:
        """
        Используя `__gettattr__`, класс предоставляет возможность
        вызывать методы API, как будто обращаясь к атрибутам.
        Пример есть в описании класса.

        :param attribute: Имя/заголовок названия метода.
        :return: Собственный инстанс класса для того,
            чтобы была возможность продолжить выстроить имя метода через точку.
        """
        if self._method_name:
            self._method_name += f".{attribute}"
        else:
            self._method_name = attribute
        return self

    async def __call__(
        self,
        __allow_cache: bool = False,
        **request_params,
    ) -> ty.Union[str, int, dict]:
        """
        Выполняет необходимый API запрос с нужным методом и параметрами,
        добавляя к ним токен и версию (может быть перекрыто).

        :param __allow_cache: Если `True` -- реузльтат запроса
            с подобными параметрами и методом будет получен из кэш-таблицы,
            если отсутсвует -- просто занесен в таблицу. Если `False` -- запрос
            просто выполнится по сети.
        :param request_params: Параметры, принимаемы методом, которые описаны в документации API.
        :return: Пришедший от API ответ.

        :raises VKAPIError: В случае ошибки, пришедшей от некорректного вызова запроса.
        """
        method_name = self._method_name
        self._method_name = ""
        return await self._make_api_request(
            method_name=method_name,
            request_params=request_params,
            allow_cache=__allow_cache,
        )

    async def fetch_token_owner_entity(self) -> PageEntity:
        """
        Возвращает сущность владельца токена.

        В зависимости от результата вызова метода `users.get`
        определяет тип владельца токена (пользователь, группа, токен сервисный)
        и задержку для запросов.

        :return: Владельца токена под соотвествующей оберткой,
            либо `Ellipsis` для сервисного токена.
        """
        if self._token_owner is None:
            # Убираем `None`, чтобы запрос строкой ниже выполнился
            self._token_owner = ...
            owner = await self.users.get()

            if owner:
                self._token_owner = User(owner[0])
                self._requests_delay = 1 / 3
            else:
                owner = await self.groups.get_by_id()
                if not owner[0]:
                    self._requests_delay = 1 / 3
                else:
                    self._token_owner = Group(owner[0])
                    self._requests_delay = 1 / 20

            return self._token_owner

        else:
            return self._token_owner

    async def method(
        self,
        __method_name: str,
        __request_params: ty.Dict[str, ty.Any],
        *,
        allow_cache: bool = False,
    ) -> ty.Union[str, int, API.default_factory]:
        """
        Выполняет необходимый API запрос с нужным методом и параметрами.

        :param __allow_cache: Если `True` -- реузльтат запроса
            с подобными параметрами и методом будет получен из кэш-таблицы,
            если отсутсвует -- просто занесен в таблицу. Если `False` -- запрос
            просто выполнится по сети.
        :param __request_params: Параметры, принимаемы методом, которые описаны в документации API.
        :return: Пришедший от API ответ.

        :raises VKAPIError: В случае ошибки, пришедшей от некорректного вызова запроса.
        """
        method_name = self._convert_name(__method_name)
        request_params = self._fill_request_params(__request_params)
        request_params = self._convert_params_for_api(request_params)
        return await self._make_api_request(
            method_name=method_name,
            request_params=request_params,
            allow_cache=allow_cache,
        )

    async def _make_api_request(
        self,
        method_name: str,
        request_params: ty.Dict[str, ty.Any],
        allow_cache: bool,
    ) -> ty.Union[str, int, API.default_factory]:
        """
        Выполняет API запрос на определнный метод с заданными параметрами

        :param method_name: Имя метода API
        :param request_params: Параметры, переданные для метода
        :param allow_cache: Использовать кэширование
        :raises VKAPIError: В случае ошибки, пришедшей от некорректного вызова запроса.
        """
        # Конвертация параметров запроса под особенности API и имени метода
        real_method_name = _convert_method_name(method_name)
        real_request_params = _convert_params_for_api(request_params)
        extra_request_params = self._stable_request_params.copy()
        extra_request_params.update(real_request_params)
        real_request_params = extra_request_params

        # Определение владельца токена нужно
        # для определения задержки между запросами
        if self._token_owner is None:
            await self.fetch_token_owner_entity()

        # Кэширование запросов по их методу и переданным параметрам
        # `cache_hash` -- ключ кэш-таблицы
        if allow_cache:
            cache_hash = urllib.parse.urlencode(real_request_params)
            cache_hash = f"{method_name}#{cache_hash}"
            if cache_hash in self._cache_table:
                return self._cache_table[cache_hash]

        # Задержка между запросами необходима по правилам API
        api_request_delay = self._get_waiting_time()
        await asyncio.sleep(api_request_delay)

        # Отправка запроса с последующей проверкой ответа
        response = await self._send_api_request(
            real_method_name, real_request_params
        )
        if "error" in response:
            raise VKAPIError.destruct_response(response)
        else:
            response = response["response"]

        # Если кэширование включено -- запрос добавится в таблицу
        if allow_cache:
            self._cache_table[cache_hash] = response

        return response

    async def _send_api_request(self, method_name: str, params: dict) -> dict:
        async with self.requests_session.post(
            self._requests_url + method_name, data=params
        ) as response:
            loaded_response = await response.json(
                loads=json_parser_policy.loads
            )
            return loaded_response

    def _get_waiting_time(self) -> float:
        """
        Рассчитывает обязательное время задержки после
        последнего API запроса. Для групп -- 0.05s,
        для пользователей/сервисных токенов -- 0.333s.

        :return: Время, необходимое для ожидания.
        """
        now = time.time()
        diff = now - self._last_request_stamp
        if diff < self._requests_delay:
            wait_time = self._requests_delay - diff
            self._last_request_stamp += wait_time
            return wait_time
        else:
            self._last_request_stamp = now
            return 0

    async def fetch_user_via_id(
        self,
        __id: ty.Union[int, str],
        *,
        fields: ty.Optional[ty.List[str]] = None,
        name_case: ty.Optional[str] = None,
    ) -> User:
        """
        Выполняет `users.get` для необходимого пользователя.
        Ответ оборачивает в спецаильную обертку пользователя.
        Более предпочтительный метод, чем сырой вызов API метода.
        Использует кэширование.

        :param __id: ID/`screen_name` пользователя.
        :param fields: Дополнительные поля в информации о пользователе.
        :param name_case: Падеж, в котором нужно вернуть пользователя.
        :return: Специальную обертку над пользователем,
            о котором запрошена информация.
        """
        users = await self.users.get(
            ...,
            user_ids=__id,
            fields=fields,
            name_case=name_case,
        )
        user = users[0]
        return User(user)

    async def fetch_users_via_ids(
        self,
        __ids: ty.Iterable[int, str],
        *,
        fields: ty.Optional[ty.List[str]] = None,
        name_case: ty.Optional[str] = None,
    ) -> ty.List[User]:
        """
        Выполняет `users.get` для необходимых пользователей.
        Ответ оборачивает в спецаильную обертку каждого пользователя.
        Более предпочтительный метод, чем сырой вызов API метода.

        :param __id: ID/`screen_name` пользователя.
        :param fields: Дополнительные поля в информации о пользователе.
        :param name_case: Падеж, в котором нужно вернуть пользователя.
        :return: Список со специальными обертками над пользователем,
            о которых запрошена информация.
        """
        users = await self.users.get(
            ...,
            user_ids=tuple(__ids),
            fields=fields,
            name_case=name_case,
        )
        wrapped_users = [User(user) for user in users]
        return wrapped_users


def _convert_param_value(__value):
    """
    Конвертирует параметер API запроса в соотвествиями
    с особенностями API и дополнительными удобствами

    :param __value: Текущее значение параметра
    :return: Новое значение параметра
    """
    # Для всех перечислений функция вызывается рекурсивно.
    # Массивы в запросе распознаются вк только если записать их как строку,
    # перечисляя значения через запятую
    if isinstance(__value, (list, set, tuple)):
        updated_sequence = map(_convert_param_value, __value)
        new_value = ",".join(updated_sequence)
        return new_value

    # Все словари, как списки, нужно сдампить в JSON
    elif isinstance(__value, dict):
        new_value = json_parser_policy.dumps(__value)
        return new_value

    # Особенности `aiohttp`
    elif isinstance(__value, bool):
        new_value = int(__value)
        return new_value

    # Если класс определяет протокол сериализации под параметр API,
    # используется соотвествующий метод
    elif isinstance(__value, APISerializable):
        new_value = __value.api_param_representation()
        return new_value

    else:
        new_value = str(__value)
        return new_value


def _convert_params_for_api(__params: dict):
    """
    Конвертирует словарь из параметров для метода API,
    учитывая определенные особенности
    :param __params: Параметры, передаваемые для вызова метода API
    :return: Новые параметры, которые можно передать
        в запрос и получить ожидаемый результат
    """
    updated_params = {
        key: _convert_param_value(value)
        for key, value in __params.items()
        if value is not None
    }
    return updated_params


def _upper_zero_group(__match: ty.Match) -> str:
    """
    Поднимает все символы в верхний
    регистр у captured-группы `let`. Используется
    для конвертации snake_case в camelCase.

    :param __match: Регекс-группа, полученная в реультате `re.sub`
    :return: Ту же букву из группы, но в верхнем регистре
    """
    return __match.group("let").upper()


def _convert_method_name(__name: str) -> str:
    """
    Конвертирует snake_case в camelCase.

    :param __name: Имя метода, который необходимо перевести в camelCase
    :return: Новое имя метода в camelCase
    """
    return re.sub(r"_(?P<let>[a-z])", _upper_zero_group, __name)