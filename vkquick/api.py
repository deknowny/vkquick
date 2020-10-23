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
import ssl
import time
import urllib.parse
import urllib.request
import typing as ty

import vkquick.exceptions
import vkquick.utils


class TokenOwner(str, enum.Enum):
    """
    Тип владельца токена. Используется
    для определения задержки между API запросами
    """

    GROUP = "group"
    USER = "user"


@dataclasses.dataclass
class API(vkquick.utils.Synchronizable):
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

    host: str = "api.vk.com"
    """
    URL отправки API запросов
    """

    response_factory: ty.Callable[
        [ty.Union[dict, list, str, int]], ty.Any
    ] = vkquick.utils.AttrDict
    """
    Обертка для ответов (по умолчанию -- `attrdict.AttrMap`,
    чтобы иметь возможность получать поля ответа через точку)
    """

    json_parser: vkquick.utils.JSONParserBase = dataclasses.field(
        default_factory=vkquick.utils.JSONParserBase.choose_parser
    )
    """
    Парсер для JSON, приходящего от ответа вк
    """

    def __post_init__(self) -> None:
        self._method_name = ""
        self._last_request_time = 0
        self.token_owner = self.define_token_owner()
        self._delay = 1 / 3 if self.token_owner == TokenOwner.USER else 1 / 20
        self.requests_session = vkquick.utils.RequestsSession(host=self.host)

    def __getattr__(self, attribute) -> API:
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
        data = urllib.parse.urlencode(request_params)
        if self.synchronized:
            return self._make_sync_api_request(method_name, data)
        return self._make_async_api_request(method_name, data)

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

    def _prepare_response_body(
        self, body: bytes
    ) -> ty.Union[str, int, API.default_factory]:
        """
        Подготавливает ответ API в надлежащий вид:
        парсит JSON, проверяет на наличие ошибок
        и оборачивает в `self.response_factory`
        """
        body = self.json_parser.loads(body)
        self._check_errors(body)
        return self.response_factory(body["response"])

    async def _make_async_api_request(
        self, method_name: str, data: str
    ) -> ty.Union[str, int, API.default_factory]:
        """
        Отправляет API запрос асинхронно с именем API метода из
        `method_name` и параметрами метода `data`, преобразованными
        в query string
        """
        await self._waiting()
        query = (
            f"GET /method/{method_name}?{data} HTTP/1.1\n"
            f"Host: {self.host}\n\n"
        )
        await self.requests_session.write(query.encode("UTF-8"))
        body = await self.requests_session.fetch_body()
        return self._prepare_response_body(body)

    def _make_sync_api_request(
        self, method_name: str, data: str
    ) -> ty.Union[str, int, API.default_factory]:
        """
        Отправляет API запрос синхронно с именем API метода из
        `method_name` и параметрами метода `data`, преобразованными
        в query string
        """
        resp = urllib.request.urlopen(
            f"https://{self.host}/method/{method_name}?{data}",
            context=ssl.SSLContext(),
        )
        body = resp.read()
        return self._prepare_response_body(body)

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

    def define_token_owner(self) -> TokenOwner:
        """
        Определяет владельца токена: группу или пользователя.
        Например, для определения задержки между запросами
        """
        with self.synchronize():
            users = self.users.get()

        return TokenOwner.USER if users() else TokenOwner.GROUP

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
