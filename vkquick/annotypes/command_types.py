from abc import ABC, abstractmethod
import re

from .base import Annotypes


class CommandArgument(Annotypes):
    ...


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
    factory = str

    def prepare(self, argname, event, func, bot, bin_stack):
        return self.factory(bin_stack.command_frame.group(argname))


class Word(CommandArgument):
    """
    A word. Eq to `\S+`
    """
    rexp = r"\S+"
    factory = str

    def prepare(self, argname, event, func, bot, bin_stack):
        return self.factory(bin_stack.command_frame.group(argname))

class List(CommandArgument):
    """
    List of smth separated by commas or whitespaces
    """
    def __init__(
        self,
        part: Annotypes,
        sep: str = r"(?:\s*,\s|\s+)",
        min_: int = 1,
        max_: int = ...
    ):
        if max_ is ...:
            max_ = ""
        else:
            max_ = str(max_)
        min_ = str(min_)

        self.rexp = f"(?:{part.rexp}(?:{sep}|$))" + "{" + f"{min_},{max_}" + "}"
        self.sep = sep
        self.part = part

    def prepare(self, argname, event, func, bot, bin_stack):
        vals = re.split(
            self.sep,
            bin_stack.command_frame.group(argname)
        )
        return [
            self.part.factory(val)
            for val in vals
        ]
