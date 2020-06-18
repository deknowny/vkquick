from abc import ABC, abstractmethod
from asyncio import iscoroutinefunction as icf
import re

from .base import Annotype
from .user import User, UserAnno


class CommandArgument(Annotype):
    factory = str


class Integer(CommandArgument):
    """
    Simple integer. Eq to `\d+`
    """

    rexp = r"\d+"
    factory = int

    def prepare(self, argname, event, func, bot, bin_stack):
        return self.factory(bin_stack.command_frame.group(argname))


class String(CommandArgument):
    """
    String part. Eq to `.+`
    """

    rexp = r".+"

    def prepare(self, argname, event, func, bot, bin_stack):
        return self.factory(bin_stack.command_frame.group(argname))


class Word(CommandArgument):
    """
    A word. Eq to `\S+`
    """

    rexp = r"\S+"

    def prepare(self, argname, event, func, bot, bin_stack):
        return self.factory(bin_stack.command_frame.group(argname))


class List(CommandArgument):
    """
    List of smth separated by commas or whitespaces
    """

    def __init__(
        self,
        part: Annotype,
        sep: str = r"(?:\s*,\s|\s+)",
        min_: int = 1,
        max_: int = ...,
    ):
        if max_ is ...:
            max_ = ""
        else:
            max_ = str(max_)
        min_ = str(min_)

        self.rexp = f"(?:{part.rexp}(?:{sep}|$))" + "{" + f"{min_},{max_}" + "}"
        self.sep = sep
        self.part = part

    async def prepare(self, argname, event, func, bot, bin_stack):
        vals = re.split(self.sep, bin_stack.command_frame.group(argname))
        self.part.bot = bot
        if icf(self.part.factory):
            return [await self.part.factory(val) for val in vals]
        else:
            return [self.part.factory(val) for val in vals]


class UserMention(CommandArgument, UserAnno):
    """
    User mention
    """

    rexp = r"\[id\d+|.+?\]"

    async def factory(self, val):
        return await User(mention=val).get_info(self.bot.api, *self.fields)

    async def prepare(self, argname, event, func, bot, bin_stack):
        mention = bin_stack.command_frame.group(argname)
        self.bot = bot
        user = await self.factory(val=mention)
        return user
