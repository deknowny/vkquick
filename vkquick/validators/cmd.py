"""
VK API li
"""
from dataclasses import dataclass, field
from typing import List
from typing import Optional
from re import fullmatch
from re import IGNORECASE

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

        if not self.prefs:
            reprefs = ""
        elif len(self.prefs) == 1:
            reprefs = self.prefs[0]
        else:
            reprefs = f"(?:{'|'.join(self.prefs)})"

        if not self.names:
            renames = ""
        elif len(self.names) == 1:
            renames = self.names[0]
        else:
            renames = f"(?:{'|'.join(self.names)})"
        self.rexp = reprefs + renames


    def __call__(self, func):
        for name, value in func.command_args.items():
            self.rexp += rf"\s*(?P<{name}>{Reaction.convert(value).rexp})"
        super().__call__(func)
        return func

    def isvalid(self, event, com, bot, bin_stack):
        matched = (
            fullmatch(self.rexp, event.object.message.text, flags=IGNORECASE)
            if self.insensetive else
            fullmatch(self.rexp, event.object.message.text)
        )
        if matched := fullmatch(self.rexp, event.object.message.text):
            bin_stack.command_frame = matched
            return (True, "")
        return (False, f"String `{event.object.message.text}` isn't matched for pattern `{self.rexp}`")
