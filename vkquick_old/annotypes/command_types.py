"""
Типы, используемые в аннотациях для построения текстовой команды в сообщении
"""
from abc import ABC, abstractmethod
from asyncio import iscoroutinefunction as icf
import re

from .base import Annotype
from vkquick.tools import User, UserAnno


class CommandArgument(Annotype):
    """
    Базовый класс для любого аннотационного типа,
    являющего аргументом текстовой команды.
    """

    factory = str
    """
    Callable структура, в которую __должно__
    быть вами обернуто возвращаемое значение.
    Принимает 1 аргумент. Создано для
    совместимость с типомами более
    __высшего__ порядка, например, `List`
    Может быть корутиной.
    """

    def prepare(self, argname, event, func, bin_stack) -> factory:
        return self.factory(bin_stack.command_frame.group(argname))


class Integer(CommandArgument):
    """
    __Целое__ число.
    Можете использовать `int` instead
    """

    rexp = r"\d+"
    factory = int


class String(CommandArgument):
    """
    Строка, состоящая как из пробельных,
    так и непробельных символов (`.+`).
    Можете использовать `str` instead
    """

    rexp = r".+"


class Word(CommandArgument):
    """
    1 слово. Состоит из непробельнных символов,
    т.е. цирфры, знаки препинания -- все это входит
    """

    rexp = r"\S+"


class List(CommandArgument):
    """
    Список каких-либо типов, разделенные каким-либо образом

    ## Параметры

    * `part`: Элемент, который будет повторяться
    (обязательно типа`CommandArgument`)

    * `sep`: Раздделитель элементов. По умолчанию это запятые и пробелы

    * `min_`: Минимальное кол-во элементов

    * `max_`: Максимальное кол-во элементов.
    `Ellipsis` означает, что максимального
    кол-ва элементов нет

    Вы также можете просто обернуть тип в [квадратные_скобки]
    """

    factory = list

    def __init__(
        self,
        part: Annotype,
        sep: str = r"(?:\s*,\s*|\s+)",
        min_: int = 1,
        max_: int = ...,
    ):
        if max_ is ...:
            max_ = ""
        else:
            max_ = str(max_)
        min_ = str(min_)

        self.rexp = (
            f"(?:{part.rexp}(?:{sep}|$))" + "{" + f"{min_},{max_}" + "}"
        )
        self.sep = sep
        self.part = part

    async def prepare(self, argname, event, func, bin_stack):
        vals = re.split(
            self.sep, bin_stack.command_frame.group(argname).rstrip()
        )
        if icf(self.part.factory):
            return [await self.part.factory(val) for val in vals]
        else:
            return [self.part.factory(val) for val in vals]


class UserMention(CommandArgument, UserAnno):
    """
    Упоминание пользователя.
    Работает __только__ на упоминание,
    т.е. поддержки ссылок и айдификаторов чиселками нет.
    Возможно, добавятся позже
    """

    rexp = r"\[id\d+\|.+?\]"

    async def factory(self, val) -> User:
        """
        Возвращает объект пользователя
        """
        return await User(mention=val).get_info(*self.fields)

    async def prepare(self, argname, event, func, bin_stack):
        mention = bin_stack.command_frame.group(argname)
        user = await self.factory(val=mention)
        return user


class Literal(CommandArgument):
    """
    Один из возможных значений. Своего рода Enum.
    Паттерн представляет собой переданный слова, разделенные `|` (или)
    """

    def __init__(self, *values):
        self.rexp = "|".join(values)


class Custom(CommandArgument):
    """
    Тип по регулярному выражению и фабрике.
    Своего рода быстрый кастомный тип без наследования
    """

    def __init__(self, rexp, factory: callable = str, /):
        self.rexp = rexp
        self.factory = factory

    async def prepare(self, argname, event, func, bin_stack):
        if icf(self.factory):
            return await self.factory(bin_stack.command_frame.group(argname))
        return self.factory(bin_stack.command_frame.group(argname))


class Optional(CommandArgument):
    """
    Делает тип опциональным,
    в случае пропуска возвращает переданный объект,
    обозначенный для умолчания, либо None
    """

    def __init__(self, elem, default=None, /):
        self.elem = elem
        self.default = default
        self.rexp = f"(?:{elem.rexp})"  # Optional made in Cmd

    async def prepare(self, argname, event, func, bin_stack):
        captured = bin_stack.command_frame.groupdict()
        if captured[argname] is None:
            return self.default

        if icf(self.elem.factory):
            return await self.elem.factory(captured[argname])
        return self.elem.factory(captured[argname])
