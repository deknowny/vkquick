"""
Типы, используемые в аннотациях для построения текстовой команды в сообщении
"""
from abc import ABC, abstractmethod
from asyncio import iscoroutinefunction as icf
import re

import typing
from vkquick import tools
from .base import Annotype
from vkquick.tools import User, UserAnno, run


class CommandArgument(Annotype):
    """
    Базовый класс для любого аннотационного типа,
    являющего аргументом текстовой команды.
    """

    factory = str
    regexp: typing.Optional[typing.AnyStr] = None
    custom_validate: bool = False
    """
    Callable структура, в которую __должно__
    быть вами обернуто возвращаемое значение.
    Принимает 1 аргумент. Создано для
    совместимость с типомами более
    __высшего__ порядка, например, `List`
    Может быть корутиной.
    """

    def has_custom_validate_method(self) -> bool:
        return self.custom_validate

    def match_regexp(self, value):
        matched = (
            re.fullmatch(self.regexp, value)
            if self.sensetive
            else re.fullmatch(
                self.regexp, value, flags=re.IGNORECASE
            )
        )
        return matched

        # f"String `{event.object.message.text}` isn't matched for pattern `{self.regexp}`",

    def validate(self, value, *, context: typing.Optional[dict] = None):
        if self.regexp is None:
            raise Exception("No regexp or custom validate method provided!")

        match = self.match_regexp(value)
        if not match:
            raise Exception()
        return self.factory(value)

    def build(self, value, context: typing.Optional[dict] = None) -> factory:
        if not self.factory:
            raise Exception("No factory or custom build method provided!")
        return self.factory(value)


class Integer(CommandArgument):
    """
    __Целое__ число.
    Можете использовать `int` instead
    """

    regexp = r"\d+"
    factory = int


class String(CommandArgument):
    """
    Строка, состоящая как из пробельных,
    так и непробельных символов (`.+`).
    Можете использовать `str` instead
    """

    regexp = r".+"


class Word(CommandArgument):
    """
    1 слово. Состоит из непробельнных символов,
    т.е. цирфры, знаки препинания -- все это входит
    """

    regexp = r"\S+"


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

    async def build(self, value, context: typing.Optional[dict] = None) -> factory:
        vals = re.split(self.sep, value.rstrip())
        return [await tools.run(self.part.build(val)) for val in vals]


class UserMention(CommandArgument, UserAnno):
    """
    Упоминание пользователя.
    Работает __только__ на упоминание,
    т.е. поддержки ссылок и айдификаторов чиселками нет.
    Возможно, добавятся позже
    """

    regexp = r"\[id\d+\|.+?\]"

    async def build(self, value, context=None) -> User:
        """
        Возвращает объект пользователя
        """
        return await User(mention=value).get_info(*self.fields)

    # async def prepare(self, argname, event, func, bin_stack):
    #     mention = bin_stack.command_frame.group(argname)
    #     user = await self.build(value=mention)
    #     return user


class Literal(CommandArgument):
    """
    Один из возможных значений. Своего рода Enum.
    Паттерн представляет собой переданный слова, разделенные `|` (или)
    """

    custom_validate = True

    def __init__(self, *values):
        self.literal_values = values
        # self.rexp = "|".join(values)

    def validate(self, value, context=None) -> None:
        if value not in self.literal_values:
            raise ValueError("Value is not in literal values!")


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
        self.rexp = f"(?:{elem.regexp})"  # Optional made in Cmd

    async def prepare(self, argname, event, func, bin_stack):
        captured = bin_stack.command_frame.groupdict()
        if captured[argname] is None:
            return self.default

        if icf(self.elem.factory):
            return await self.elem.factory(captured[argname])
        return self.elem.factory(captured[argname])
