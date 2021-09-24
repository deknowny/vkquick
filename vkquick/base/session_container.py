from __future__ import annotations

import contextlib
import ssl
import typing

import aiohttp

from vkquick.json_parsers import BaseJSONParser, json_parser_policy


class SessionContainerMixin:
    """
    Этот класс позволяет удобным способ содержать инстанс `aiohttp.ClientSession`.
    Поскольку инициализации сессии может происходить только уже с запущенным циклом
    событий, это может вызывать некоторые проблемы при попытке создать
    сессию внутри `__init__`.

    Кроме хранения сессию, к которой внутри вашего класса можно
    обратится через `requests_session`, этот класс позволяет передавать
    кастомные сессии `aiohttp` и JSON-парсеры. Используйте соответствующие аргументы
    в `__init__` своего класса, чтобы предоставить возможность пользователю передать
    собственные имплементации или сессию со своими настройками.
    """

    def __init__(
        self,
        *,
        requests_session: typing.Optional[aiohttp.ClientSession] = None,
        json_parser: typing.Optional[BaseJSONParser] = None
    ) -> None:
        """
        Arguments:
            requests_session: Кастомная `aiohttp`-сессия для HTTP запросов.
            json_parser: Кастомный парсер, имплементирующий методы
                сериализации/десериализации JSON.
        """
        self.__session = requests_session
        self.__json_parser = json_parser or json_parser_policy

    @property
    def requests_session(self) -> aiohttp.ClientSession:
        """
        Возвращает сессию, которую можно использовать для
        отправки запросов. Если сессия еще не была создана,
        произойдет инициализация. Не рекомендуется использовать
        этот проперти вне корутин.
        """
        if self.__session is None or self.__session.closed:
            self.__session = self._init_aiohttp_session()

        return self.__session

    async def __aenter__(self) -> SessionContainerMixin:
        """
        Позволяет автоматически закрыть сессию
        запросов по выходу из `async with` блока.
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close_session()

    async def close_session(self) -> None:
        """
        Закрывает используемую `aiohttp` сессию.
        Можно использовать асинхронный менеджер контекста
        вместо этого метода.
        """
        if self.__session is not None:
            await self.__session.close()

    async def parse_json_body(
        self, response: aiohttp.ClientResponse, **kwargs
    ) -> dict:
        """
        Используйте в классе вместо прямого использования `.json()`
        для получения JSON из body ответа. Этот метод использует
        переданный JSON парсер в качестве десериализатора.

        Arguments:
            response: Ответ, пришедший от отправки запроса.
            kwargs: Дополнительные поля, которые будут переданы
                в `.json()` помимо JSON-десериализатора.

        Returns:
            Словарь, полученный при декодировании ответа.
        """
        return await response.json(loads=self.__json_parser.loads, **kwargs)

    def _init_aiohttp_session(self) -> aiohttp.ClientSession:
        """
        Инициализирует `aiohttp`-сессию. Переопределяйте этот метод
        в своем классе, чтобы установить другие настройки сессии по умолчанию.

        Returns:
            Новую `aiohttp`-сессию
        """
        return aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=ssl.SSLContext()),
            skip_auto_headers={"User-Agent"},
            raise_for_status=True,
            json_serialize=self.__json_parser.dumps,
        )

    async def refresh_session(self) -> None:
        if not self.__session.closed:
            with contextlib.suppress(Exception):
                await self.__session.close()
        self.__session = self._init_aiohttp_session()
