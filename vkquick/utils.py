"""
Тривиальные инструменты для некоторых кейсов
"""
import abc
import asyncio
import random
import ssl
import json
import functools
import os
import typing as ty

try:
    import orjson
except ImportError:
    orjson = None


T = ty.TypeVar("T")


def peer(chat_id: int) -> int:
    """
    Добавляет к `chat_id` значение, чтобы оно стало `peer_id`.
    Кртакая и более приятная запись сложения любого числа с 2 000 000 000
    (да, на один символ)

    peer_id=vq.peer(123)
    """
    return 2_000_000_000 + chat_id


async def sync_async_run(
    obj: ty.Union[T, ty.Awaitable]
) -> ty.Union[T, ty.Any]:
    """
    Если `obj` является корутинным объектом --
    применится `await`. В ином случае, вернется само переданное значение
    """
    if asyncio.iscoroutine(obj):
        return await obj
    return obj


def random_id(side: int = 2 ** 31 - 1) -> int:
    """
    Случайное число в дипазоне +-`side`.
    Используется для API метода `messages.send`
    """
    return random.randint(-side, +side)


class SafeDict(dict):
    """
    Обертка для словаря, передаваемого в `str.format_map`
    (формат с возможными пропусками)
    """

    def __missing__(self, key):
        return "{" + key + "}"


class AttrDict:
    """
    Надстройка к словарю для возможности получения
    значений через точку. Работает рекурсивно,
    поддержка списков также имеется.

        foo = AttrDict({"a": {"b": 1}})
        print(foo.a.b)  # 1

        foo = AttrDict([{"a": [{"b": 1}]}])
        print(foo[0].a[0].b)  # 1

        # Когда ключ нельзя получить через атрибут
        foo = AttrDict({"#$@234": 1})
        print(foo("#$@234"))  # 1

        # Нужно получить исходный объект
        foo = AttrDict({"a": 1})
        print(foo())  # {'a': 1}

        foo = AttrDict({})
        foo.a = 1  # foo["a"] = 1
        print(foo())  # {'a': 1}

        # `__getitem__` возвращает исходный объект.
        # `__call__` -- новую обертку AttrDict
        foo = AttrDict({"a": {"b": 1}})
        print(isinstance(foo.a, AttrDict))  # True
        print(isinstance(foo["a"], dict))  # True
    """
    def __new__(cls, mapping):
        if isinstance(mapping, dict):
            self = object.__new__(cls)
            self.__init__(mapping)
            return self
        if isinstance(mapping, list):
            return [cls(i) for i in mapping]

        else:
            return mapping

    def __init__(self, mapping):
        object.__setattr__(self, "mapping_", mapping)

    def __getattr__(self, item):
        return self.__class__(self.mapping_[item])

    def __repr__(self):
        return f"{self.__class__.__name__}({self.mapping_})"

    def __call__(self, item=None):
        if item is None:
            return self.mapping_
        return self.__getattr__(item)

    def __getitem__(self, item):
        return self.mapping_[item]

    def __contains__(self, item):
        return item in self.mapping_

    def __setattr__(self, key, value):
        self.mapping_[key] = value

    def __setitem__(self, key, value):
        self.__setattr__(key, value)


class RequestsSession:
    """
    Надстройка над асинхронным TCP клиентом.
    В момент инициализации принимает `host`,
    к которому в последующем можно отправлять запросы.
    Советуем использовать `HTTP/1.1`, либо `1.0`
    с хедером `Connection: Keep-Alive`.
    """
    def __init__(self, host: str) -> None:
        self.writer = self.reader = None
        self.host = host
        self.lock = asyncio.Lock()

    async def _setup_connection(self) -> None:
        """
        Устанавливает TCP соединение, присваивая
        `StreamReader` и `StreamWriter` в поля объекта
        """
        self.reader, self.writer = await asyncio.open_connection(
            self.host, 443, ssl=ssl.SSLContext()
        )

    async def write(self, body_query: bytes) -> None:
        """
        Записывает в сокет HTTP сообщение, перед
        этим дожидаясь его очищения (`drain()`).
        В случае, если соединение разорвалось,
        устанавливает его еще раз
        """
        if self.writer is None:
            await self._setup_connection()
        try:
            await self.writer.drain()
        except ConnectionResetError:
            await self._setup_connection()
        finally:
            self.writer.write(body_query)

    async def fetch_body(self) -> bytes:
        """
        Читает из сокета HTTP ответ. Путем
        нехитрых манипуляций достает `Content-Length`,
        читает body респонза и возвращает именно его в байтах
        """
        async with self.lock:
            while True:
                line = await self.reader.readline()
                if line.startswith(b"Content-Length"):
                    content_length = self._get_content_length(line)
                if line == b"\r\n":
                    break

            body = await self.reader.read(content_length)
            return body

    @staticmethod
    def _get_content_length(line: bytes) -> int:
        """
        Достает числовое значение из `Content-Length` хедера
        """
        line = line.decode("utf-8")
        length = ""
        for letter in line:
            if letter.isdigit():
                length += letter
        length = int(length)
        return length

    def __del__(self) -> None:
        if self.writer is not None:
            self.writer.close()


class JSONParserBase(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def dumps(data: ty.Dict[str, ty.Any]) -> str:
        ...

    @staticmethod
    @abc.abstractmethod
    def loads(string: ty.Union[str, bytes]) -> ty.Dict[str, ty.Any]:
        ...

    @staticmethod
    def choose_parser():
        if orjson is None:
            return BuiltinJSONParser
        return OrjsonJSONParser


class BuiltinJSONParser(JSONParserBase):

    dumps = functools.partial(
        json.dumps, ensure_ascii=False, separators=(",", ":")
    )
    loads = json.loads


class OrjsonJSONParser(JSONParserBase):
    @staticmethod
    def dumps(data: ty.Dict[str, ty.Any]) -> str:
        return str(orjson.dumps(data))

    @staticmethod
    def loads(string: ty.Union[str, bytes]) -> ty.Dict[str, ty.Any]:
        return orjson.loads(string)


def clear_console():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


class Synchronizable:
    """
    Протокол для синхронизации объектов

    Некоторое поведение объектов может быть
    асинхронным (например, вызов API методов),
    но использовать те же возможности, когда весь код строится
    синхронно и конкурировать нечему, не нужно.
    Поэтому этот класс определяет общее поведение для
    объектов, чье поведение должно стать синхронным.
    """

    __synchronized = False  # По умолчанию асинхронно

    @property
    def synchronized(self):
        """
        Состояние режима объекта: асинхронный/синхронный
        """
        return self.__synchronized

    def synchronize(self):
        """
        Метод, меняющий поведение на синхронное.
        Если вы меняете поведение разово, используйте
        вместе с менеджером контекста:

            with obj.synchronize():
                obj.some_method_that_was_async_but_now_sync()
        """
        self.__synchronized = True
        return self

    def __enter__(self):
        """
        Менеджер контекста гарантирует, что
        поведение объекта обратно поменяется на асинхронное
        """

    def __exit__(self, *args):
        self.__synchronized = False
