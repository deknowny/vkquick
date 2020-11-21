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
import functools
import enum
import re
import time
import urllib.parse
import typing as ty

import aiohttp
import cachetools
import requests

from vkquick.base.json_parser import JSONParser
from vkquick.json_parsers import BuiltinJSONParser
from vkquick.base.synchronizable import Synchronizable
from vkquick.exceptions import VkApiError
from vkquick.utils import AttrDict
from vkquick.wrappers.user import User
from vkquick.events_generators.longpoll import GroupLongPoll, UserLongPoll


class TokenOwner(str, enum.Enum):
    """
    Тип владельца токена. Используется
    для определения задержки между API запросами
    """

    GROUP = "group"
    USER = "user"


@dataclasses.dataclass
class API(Synchronizable):
    """
    Обертка для API запросов

    Допустим, вам нужно вызвать метод `messages.getConversationsById`
    и передать параметры `peer_ids=2000000001`. Сделать это можно несколькими способами

    > Вызов метода делается через `await`, т.е. внутри корутинных функций (`async def`)

    1. Через `.method`


        import vkquick as vq


        api = vq.API("mytoken")
        # Про синхронизаторы будет позже
        with api.synchronize():
            api.method("messages.getConversationsById", {"peer_ids": vq.peer(1)})


    > `vq.peer` прибавит к числу 2_000_000_000

    2. Через `__getattr__` с последующим `__call__`


        import vkquick as vq


        api = vq.API("mytoken")
        with api.synchronize():
            api.messages.getConversationsById(peer_ids=vq.peer(1))


    VK Quick может преобразовать camelCase в snake_case:


        import vkquick as vq


        api = vq.API("mytoken")
        with api.synchronize():
            # Вызовет метод `messages.getConversationsById`
            await api.messages.get_conversations_by_id(peer_ids=vq.peer(1))


    По умолчанию запросы асинхронные и их можно await'ить или
    создавать таски

        import asyncio

        import vkquick as vq


        api = vq.API("mytoken")
        async def main():
            response = await api.messages.get_conversations_by_id(
                peer_ids=vq.peer(1)
            )
            print(response)

        asyncio.run(main())

    Автокомплит

    Представим, что вы хотите передать `group_id`. Вы используете много методов,
    где передаете один и тот же `group_id`. Чтобы не повторять себя жеб
    можно сделать вот так:


        import vkquick as vq


        api = vq.API("mytoken", autocomplete_params={"group_id": 123})
        with api.synchronize():
            api.messages.get_conversations_by_id(
                ...,  # Подстановка `Ellipsis` первым аргументом вызывает автокомплит
                peer_ids=vq.peer(1)
            )


    Теперь метод вызвался с двумя параметрами: `group_id` и `peer_ids`

    Фабрика ответов

    По умолчанию, ответы оборачиваются в специальный класс `AttrDict`,
    чтобы поля ответа можно было получить через точку


        import vkquick as vq


        api = vq.API("mytoken")
        with api.synchronize():
            convs = await api.messages.get_conversations_by_id(
                peer_ids=vq.peer(1)
            )

            # Аналогично convs[0]["chat_settings"]["title"]
            name = convs[0].chat_settings.title


    Если вы хотите использовать свою обертку на словари, установите `response_factory`
    при инициализации

    Синхронизация

    Бывают случаи, когда асинхронность лишь мешает. Этот класс
    предоставляет функционал для синхронных запросов, определяя
    интерфейс `Synchronizable`:

        import vkquick as vq

        api = vq.API("mytoken")
        with api.synchronize():
            users = api.users.get(user_ids=1)  # `await` не нужен
        # Либо:
        # with api.synchronize():
        #     users = api.method("users.get", user_ids=1)
        print(users)


    Кэширование

    Вы можете кэшировать некоторые запросы для ускорения.
    Кэш производится по отправленным параметрам и вызванному методу.
    Доступен как синхронному, так и асинхронному API

    import vkquick as vq

        api = vq.API("mytoken")
        with api.synchronize():

            # Обычный запрос
            api.users.get(allow_cache=True, user_ids=1)

            # Этот вызов будет гораздо быстрее, т.к.
            # Данные достанутся из кэша
            api.users.get(allow_cache=True, user_ids=1)

    """

    token: str
    """
    Access Token для API запросов
    """

    autocomplete_params: ty.Dict[str, ty.Any] = dataclasses.field(default_factory=dict)
    """
    При вызове API метода первым аргументом можно передать Ellipsis,
    тогда в вызов подставятся поля из этого аргумента 
    """

    version: ty.Union[float, str] = "5.133"
    """
    Версия API
    """

    response_factory: ty.Callable[
        [ty.Union[dict, list, str, int]], ty.Any
    ] = dataclasses.field(default=AttrDict)
    """
    Обертка для ответов (по умолчанию -- `vkquick.utils.AttrMap`,
    чтобы иметь возможность получать поля ответа через точку)
    """

    URL: str = "https://api.vk.com/method/"
    """
    URL для API запросов. 
    """

    json_parser: ty.Optional[ty.Type[JSONParser]] = None
    """
    Парсер для JSON, приходящего от ответа вк
    """

    token_owner: ty.Optional[TokenOwner] = None
    """
    Владелец токена: пользователь/группа. если не передано,
    определяется автоматически через `users.get`. Внутри используется
    для определения задержки между запросами
    """

    class Config:
        arbitrary_types_allowed = False

    def __post_init__(self) -> None:
        self.json_parser = self.json_parser or BuiltinJSONParser
        self.async_http_session = None
        self.sync_http_session = requests.Session()
        self.cache_table = cachetools.TTLCache(
            ttl=3600, maxsize=2 ** 15
        )
        self._method_name = ""
        self._last_request_time = 0
        self._delay = 0
        self.token_owner = self.token_owner or self._define_token_owner()
        self._delay = 1 / 3 if self.token_owner == TokenOwner.USER else 1 / 20

    @functools.cached_property
    def token_owner_user(self) -> User:
        """
        Владелец токена (объект пользовтаеля).
        Только если токеном владеет юзер
        """
        with self.synchronize():
            user = self.users.get()
            user = User.parse_obj(user[0])
            return user

    def __getattr__(self, attribute: str) -> API:
        """
        Выстраивает имя метода путем переложения
        имен API методов на "получение атрибутов".

        Например

        ```python
        await API(...).messages.send(...)
        ```

        Вызовет API метод `messages.send`. Также есть
        поддержка конвертации snake_case в camelCase:
        """
        attribute = self._convert_name(attribute)
        if self._method_name:
            self._method_name += f".{attribute}"
        else:
            self._method_name = attribute
        return self

    def __call__(
        self,
        use_autocomplete_params_: bool = False,
        /,
        allow_cache_: bool = False,
        **request_params,
    ) -> ty.Union[str, int, API.default_factory]:
        """
        Вызывает API запрос с именем метода, полученным через
        `__getattr__`, и параметрами из `**request_params`

        В случае некорректного запроса поднимается ошибка
        `vkquick.exceptions.VkApiError`

        `allow_cache` разрешает кэшировать текущий запрос
        и использовать значение из кэша, если такое есть
        """
        method_name = self._convert_name(self._method_name)
        request_params = self._fill_request_params(request_params)
        if use_autocomplete_params_:
            request_params = {**self.autocomplete_params, **request_params}
        self._method_name = ""
        return self._route_request_scheme(
            method_name=method_name,
            request_params=request_params,
            allow_cache=allow_cache_,
        )

    def method(
        self,
        method_name: str,
        request_params: ty.Dict[str, ty.Any],
        /,
        *,
        allow_cache: bool = False,
    ) -> ty.Union[str, int, API.default_factory]:
        """
        Вызывает API запрос, передавая имя метода (`method_name`)
        и его параметры (`request_params`).
        Токен и версия API могут быть перекрыты значениями из `request_params`

        В случае некорректного запроса поднимается ошибка
        `vkquick.exceptions.VkApiError`

        `allow_cache` разрешает кэшировать текущий запрос
        и использовать значение из кэша, если такое есть
        """
        method_name = self._convert_name(method_name)
        request_params = self._fill_request_params(request_params)
        return self._route_request_scheme(
            method_name=method_name,
            request_params=request_params,
            allow_cache=allow_cache,
        )

    def _route_request_scheme(
        self,
        method_name: str,
        request_params: ty.Dict[str, ty.Any],
        allow_cache: bool,
    ) -> ty.Union[str, int, API.default_factory]:
        """
        Определяет, как вызывается запрос: синхронно или асинхронно
        в зависимости от того значения синхронизации
        """
        request_params = self._convert_collections_params(request_params)
        if self.is_synchronized:
            return self._make_sync_api_request(
                method_name, request_params, allow_cache
            )
        return self._make_async_api_request(
            method_name, request_params, allow_cache
        )

    @staticmethod
    def _convert_collections_params(
        params: ty.Dict[str, ty.Any], /
    ) -> ty.Dict[str, ty.Any]:
        """
        Лучшее API в Интернете не может распарсить массивы,
        поэтому все перечисления нужно собирать в строку и разделять запятой

        Для справки, вот так передается значение `{"foo": ["fizz", "bazz"]}`:

        `?foo=fizz&foo=bazz`

        Но приходится вот так (%2C - запятая по стандарту):

        `?foo=fizz%2Cbazz %2C - запятая по стандарту

        + со временем сюда добавились еще некоторые преобразования
        """
        new_params = {}
        for key, value in params.items():
            if isinstance(value, (list, set, tuple)):
                new_params[key] = ",".join(map(str, value))

            # Для aiohttp
            elif isinstance(value, bool):
                new_params[key] = int(value)

            elif value is None:
                continue
            else:
                new_params[key] = str(value)

        return new_params

    def _prepare_response_body(
        self, body: ty.Dict[str, ty.Any]
    ) -> ty.Union[str, int, API.default_factory]:
        """
        Подготавливает ответ API в надлежащий вид:
        парсит JSON, проверяет на наличие ошибок
        и оборачивает в `self.response_factory`
        """
        self._check_errors(body)
        return self.response_factory(body["response"])

    @staticmethod
    def _build_cache_hash(
        method_name: str, data: ty.Dict[str, ty.Any]
    ) -> str:
        """
        Создает хеш для кэш-таблицы, по которому можно
        будет в последующем достать уже отправленный
        когда-либо запрос
        """
        cache_hash = urllib.parse.urlencode(data)
        cache_hash = f"{method_name}#{cache_hash}"
        return cache_hash

    # Need a decorator-factory?
    async def _make_async_api_request(
        self, method_name: str, data: ty.Dict[str, ty.Any], allow_cache: bool
    ) -> ty.Union[str, int, API.default_factory]:
        """
        Отправляет API запрос асинхронно с именем API метода из
        `method_name` и параметрами метода `data`, преобразованными
        в query string
        """
        if allow_cache:
            cache_hash = self._build_cache_hash(method_name, data)
            if cache_hash in self.cache_table:
                return self.cache_table[cache_hash]
            await asyncio.sleep(self._get_waiting_time())
            response = await self.send_async_api_request(
                path=method_name, params=data
            )
            response = self._prepare_response_body(response)
            self.cache_table[cache_hash] = response
            return response

        await asyncio.sleep(self._get_waiting_time())
        response = await self.send_async_api_request(
            path=method_name, params=data
        )
        return self._prepare_response_body(response)

    async def send_async_api_request(self, path, params):
        if self.async_http_session is None:
            self.async_http_session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False),
                skip_auto_headers={"User-Agent"},
                raise_for_status=True,
                json_serialize=self.json_parser.dumps,
            )
        async with self.async_http_session.get(
            f"{self.URL}{path}", params=params
        ) as response:
            loaded_response = await response.json(loads=self.json_parser.loads)
            return loaded_response

    def _make_sync_api_request(
        self, method_name: str, data: ty.Dict[str, ty.Any], allow_cache: bool
    ) -> ty.Union[str, int, API.default_factory]:
        """
        Отправляет API запрос синхронно с именем API метода из
        `method_name` и параметрами метода `data`, преобразованными
        в query string
        """
        if allow_cache:
            cache_hash = self._build_cache_hash(method_name, data)
            if cache_hash in self.cache_table:
                return self.cache_table[cache_hash]
            time.sleep(self._get_waiting_time())
            response = self.send_sync_api_request(
                path=method_name, params=data
            )
            response = self._prepare_response_body(response)
            self.cache_table[cache_hash] = response
            return response
        time.sleep(self._get_waiting_time())
        response = self.send_sync_api_request(
            path=method_name, params=data
        )
        return self._prepare_response_body(response)

    def send_sync_api_request(self, path, params):
        response = self.sync_http_session.get(
            f"{self.URL}{path}", params=params
        )
        json_response = self.json_parser.loads(response.content)
        return json_response

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

    @classmethod
    def _convert_name(cls, name: str) -> str:
        """
        Конвертирует snake_case в camelCase
        """
        return re.sub(r"_(?P<let>[a-z])", cls._upper_zero_group, name)

    @staticmethod
    def _check_errors(response: ty.Dict[str, ty.Any]) -> None:
        """
        Проверяет, является ли ответ от вк ошибкой
        """
        if "error" in response:
            raise VkApiError.destruct_response(response)

    def _define_token_owner(self) -> TokenOwner:
        """
        Определяет владельца токена: группу или пользователя.
        Например, для определения задержки между запросами
        """
        with self.synchronize():
            users = self.users.get()

        return TokenOwner.USER if users() else TokenOwner.GROUP

    def _get_waiting_time(self) -> float:
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
            return wait_time
        else:
            self._last_request_time = now
            return 0

    async def close_session(self):
        """
        Закрывает соединение сессии
        """
        await self.async_http_session.close()

    async def fetch_user_via_id(self,
        id_: ty.Union[int, str],
        /,
        *,
        fields: ty.Optional[ty.List[str]] = None,
        name_case: ty.Optional[str] = None,
    ) -> User:
        """
        Создает обертку над юзером через его ID или screen name
        """
        users = await self.users.get(
            allow_cache_=True,
            user_ids=id_,
            fields=fields,
            name_case=name_case,
        )
        user = users[0]
        return User.parse_obj(user)

    async def fetch_user_via_ids(self,
        ids: ty.Union[int, str],
        /,
        *,
        fields: ty.Optional[ty.List[str]] = None,
        name_case: ty.Optional[str] = None,
    ) -> ty.Tuple[User, ...]:
        """
        Создает обертку над юзером через его ID или screen name
        """
        users = await self.users.get(
            allow_cache_=True,
            user_ids=ids,
            fields=fields,
            name_case=name_case,
        )
        users = tuple(User.parse_obj(user) for user in users)
        return users

    def init_group_lp(self, **kwargs) -> GroupLongPoll:
        return GroupLongPoll(self, **kwargs)

    def init_user_lp(self, **kwargs) -> UserLongPoll:
        return UserLongPoll(self, **kwargs)