"""
VK API li
"""
from dataclasses import dataclass, field
from typing import List
from typing import Optional
from re import fullmatch

from .base import Validator
from vkquick import Reaction


class Cmd(Validator):
    """
    Use for bot's commands
    """

    def __init__(
        self,
        *,
        prefs: Optional[List[str]] = None,
        names: Optional[List[str]] = None,
        insensetive: bool = True,
    ):
        self.prefs = [] if prefs is None else prefs
        self.names = [] if names is None else names
        self.insensetive = insensetive

        self.rexp = rf"(?:{'|'.join(self.prefs)})" rf"(?:{'|'.join(self.names)})"

    def __call__(self, func):
        for name, value in func.command_args.items():
            self.rexp += rf"\s*(?P<{name}>{Reaction.convert(value).rexp})"
        super().__call__(func)
        return func

    def isvalid(self, event, com, bot, bin_stack):
        if matched := fullmatch(self.rexp, event.object.message.text):
            bin_stack.command_frame = matched
            return True
        return False
