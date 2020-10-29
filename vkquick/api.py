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
import re
import time
import typing as ty

import vkquick.base.json_parser
import vkquick.base.synchronizable
import vkquick.exceptions
import vkquick.utils
import vkquick.clients
import vkquick.base.client


class TokenOwner(str, enum.Enum):
    """
    Тип владельца токена. Используется
    для определения задержки между API запросами
    """

    GROUP = "group"
    USER = "user"


@dataclasses.dataclass
class API(vkquick.base.synchronizable.Synchronizable):
    """
    Обертка для API запросов

    Допустим, вам нужно вызвать метод `messages.getConversationsById`
    и передать параметры `peer_ids=2000000001`. Сделать это можно несколькими способами

    > Вызов метода делается через `await`, т.е. внутри корутинных функций (`async def`)

    1. Через `.method`


        import vkquick as vq

        api = vq.API("mytoken")
        await api.method("messages.getConversationsById", {"peer_ids": vq.peer(1)})


    > `vq.peer` прибавит к числу 2_000_000_000

    2. Через `__getattr__` с последующим `__call__`


        import vkquick as vq

        api = vq.API("mytoken")
        await api.messages.getConversationsById(peer_ids=vq.peer(1))


    VK Quick может преобразовать camelCase в snake_case:


        import vkquick as vq

        api = vq.API("mytoken")
        await api.messages.get_conversations_by_id(peer_ids=vq.peer(1))


    Автокомплит

    Представим, что вы хотите передать `group_id`. Вы используете много методов,
    где передаете один и тот же `group_id`. Чтобы не повторять себя жеб
    можно сделать вот так:


        import vkquick as vq

        api = vq.API("mytoken", autocomplete_params={"group_id": 123})
        await api.messages.get_conversations_by_id(
            ...,  # Подстановка `Ellipsis` первым аргументом вызывает автокомплит
            peer_ids=vq.peer(1)
        )


    Теперь метод вызвался с двумя параметрами: `group_id` и `peer_ids`

    Фабрика ответов

    По умолчанию, ответы оборачиваются в специальный класс `AttrDict`,
    чтобы поля ответа можно было получить через точку


        import vkquick as vq

        api = vq.API("mytoken")
        convs = await api.messages.get_conversations_by_id(
            peer_ids=vq.peer(1)
        )
        name = convs[0].chat_settings.title  # Аналогично convs[0]["chat_settings"]["title"]


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
    """

    token: str
    """
    Access Token для API запросов
    """

    version: ty.Union[float, str] = "5.133"
    """
    Версия API
    """

    autocomplete_params: ty.Dict[str, ty.Any] = dataclasses.field(
        default_factory=dict
    )
    """
    При вызове API метода первым аргументом можно передать Ellipsis,
    тогда в вызов подставятся поля из этого аргумента 
    """

    response_factory: ty.Callable[
        [ty.Union[dict, list, str, int]], ty.Any
    ] = vkquick.utils.AttrDict
    """
    Обертка для ответов (по умолчанию -- `attrdict.AttrMap`,
    чтобы иметь возможность получать поля ответа через точку)
    """

    json_parser: ty.Optional[
        ty.Type[vkquick.base.json_parser.JSONParser]
    ] = None
    """
    Парсер для JSON, приходящего от ответа вк
    """

    token_owner: ty.Optional[TokenOwner] = None
    """
    Владелец токена: пользователь/группа. если не передано,
    определяется автоматически через `users.get`. Внутри используется
    для определения задержки между запросами
    """

    async_http_session: ty.Optional[
        vkquick.base.client.AsyncHTTPClient
    ] = None

    sync_http_session: ty.Optional[vkquick.base.client.SyncHTTPClient] = None

    def __post_init__(self) -> None:
        self.json_parser = (
            self.json_parser or vkquick.json_parsers.BuiltinJSONParser
        )
        self.async_http_session = (
            self.async_http_session
            or vkquick.clients.AIOHTTPClient(
                url="https://api.vk.com/method/",
                json_parser=self.json_parser,
            )
        )
        self.sync_http_session = (
            self.sync_http_session
            or vkquick.clients.RequestsHTTPClient(
                url="https://api.vk.com/method/",
                json_parser=self.json_parser,
            )
        )
        self._method_name = ""
        self._last_request_time = 0
        self._delay = 0
        self.token_owner = self.token_owner or self._define_token_owner()
        self._delay = 1 / 3 if self.token_owner == TokenOwner.USER else 1 / 20

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
        self, use_autocomplete_params_: bool = False, /, **request_params
    ) -> ty.Union[str, int, API.default_factory]:
        """
        Вызывает API запрос с именем метода, полученным через
        `__getattr__`, и параметрами из `**request_params`

        В случае некорректного запроса поднимается ошибка
        `vkquick.exceptions.VkApiError`
        """
        method_name = self._convert_name(self._method_name)
        request_params = self._fill_request_params(request_params)
        if use_autocomplete_params_:
            request_params = {**self.autocomplete_params, **request_params}
        self._method_name = ""
        return self._route_request_scheme(
            method_name=method_name, request_params=request_params
        )

    def method(
        self, method_name: str, request_params: ty.Dict[str, ty.Any], /
    ) -> ty.Union[str, int, API.default_factory]:
        """
        Вызывает API запрос, передавая имя метода (`method_name`)
        и его параметры (`request_params`).
        Токен и версия API могут быть перекрыты значениями из `request_params`

        В случае некорректного запроса поднимается ошибка
        `vkquick.exceptions.VkApiError`
        """
        method_name = self._convert_name(method_name)
        request_params = self._fill_request_params(request_params)
        return self._route_request_scheme(
            method_name=method_name, request_params=request_params
        )

    def _route_request_scheme(
        self, method_name: str, request_params: ty.Dict[str, ty.Any]
    ) -> ty.Union[str, int, API.default_factory]:
        """
        Определяет, как вызывается запрос: синхронно или асинхронно
        в зависимости от того значения синхронизации
        """
        self._convert_collections_params(request_params)
        if self.synchronized:
            return self._make_sync_api_request(method_name, request_params)
        return self._make_async_api_request(method_name, request_params)

    @staticmethod
    def _convert_collections_params(params: ty.Dict[str, ty.Any], /) -> None:
        """
        Лучшее API в Интернете не может распарсить массивы,
        поэтому все перечисления нужно собирать в строку и разделять запятой

        Для справки, вот так передается значение `{"foo": ["fizz", "bazz"]}`:

        `?foo=fizz&foo=bazz`

        Но приходится вот так (%2C - запятая по стандарту):

        `?foo=fizz%2Cbazz %2C - запятая по стандарту
        """
        for key, value in params.items():
            if isinstance(value, (list, set, tuple)):
                params[key] = ",".join(map(str, value))

            # For aiohttp
            elif isinstance(value, bool):
                params[key] = int(value)

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

    async def _make_async_api_request(
        self, method_name: str, data: ty.Dict[str, ty.Any]
    ) -> ty.Union[str, int, API.default_factory]:
        """
        Отправляет API запрос асинхронно с именем API метода из
        `method_name` и параметрами метода `data`, преобразованными
        в query string
        """
        await asyncio.sleep(self._get_waiting_time())
        response = await self.async_http_session.send_get_request(
            path=method_name, params=data
        )
        return self._prepare_response_body(response)

    def _make_sync_api_request(
        self, method_name: str, data: ty.Dict[str, ty.Any]
    ) -> ty.Union[str, int, API.default_factory]:
        """
        Отправляет API запрос синхронно с именем API метода из
        `method_name` и параметрами метода `data`, преобразованными
        в query string
        """
        time.sleep(self._get_waiting_time())
        response = self.sync_http_session.send_get_request(
            path=method_name, params=data
        )
        return self._prepare_response_body(response)

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
            raise vkquick.exceptions.VkApiError.destruct_response(response)

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
        await self.async_http_session.close()
