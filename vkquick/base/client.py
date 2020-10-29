import abc
import typing as ty

import vkquick.base.json_parser


class _HTTPClient(abc.ABC):
    """
    Фабрика для базовых HTTP клиентов
    """

    @abc.abstractmethod
    def __init__(
        self, url: str, json_parser: vkquick.base.json_parser.JSONParser
    ):
        pass


class SyncHTTPClient(_HTTPClient):
    """
    Синхронный HTTP клиент
    """

    @abc.abstractmethod
    def send_get_request(
        self, path: str, params: ty.Dict[str, ty.Any]
    ) -> ty.Dict[str, ty.Any]:
        """
        Отправляет HTTP запрос и парсит JSON из тела респонза,
        возвращая словарь
        """


class AsyncHTTPClient(_HTTPClient, abc.ABC):
    """
    Асинхронный HTTP клиент
    """

    @abc.abstractmethod
    async def send_get_request(
        self, path: str, params: ty.Dict[str, ty.Any]
    ) -> ty.Dict[str, ty.Any]:
        """
        Отправляет HTTP запрос и парсит JSON из тела респонза,
        возвращая словарь
        """

    @abc.abstractmethod
    async def close(self):
        """
        Закрытие сессии
        """
