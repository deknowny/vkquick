from __future__ import annotations

import typing as ty

import pygments.formatters
import pygments.formatters.terminal
import pygments.token

from vkquick.utils import cached_property
from vkquick.wrappers.message import Message

pygments.formatters.terminal.TERMINAL_COLORS[
    pygments.token.string_to_tokentype("String")
] = ("gray", "_")
pygments.formatters.terminal.TERMINAL_COLORS[
    pygments.token.string_to_tokentype("Token.Literal.Number")
] = ("yellow", "_")
pygments.formatters.terminal.TERMINAL_COLORS[
    pygments.token.string_to_tokentype("Token.Keyword.Constant")
] = ("red", "_")
pygments.formatters.terminal.TERMINAL_COLORS[
    pygments.token.string_to_tokentype("Token.Name.Tag")
] = ("cyan", "_")


class Event:
    """
    Обертка для приходящего события в виде словаря.
    Позволяет обращаться к полям события как к атрибутам
    """

    def __init__(self, value):
        super().__init__(value)
        object.__setattr__(self, "_message", None)

    @cached_property
    def from_group(self):
        if isinstance(self(), list):
            return False
        return True

    @cached_property
    def type(self) -> ty.Union[str, int]:
        if isinstance(self(), list):
            return self[0]
        return self["type"]

    @cached_property
    def event_id(self) -> ty.Union[str, int]:
        if isinstance(self(), list):
            return self[1]
        return self["event_id"]

    @property
    def msg(self) -> Message:
        if self._message is not None:
            return Message(self._message)
        if self.type not in ("message_new", "message_reply", 4):
            raise TypeError(
                f"Can't get message if event.type is `{self.type}`"
            )
        if "message" in self.object:
            return Message(self.object.message)
        return Message(self.object)

    # Здесь нельзя использовать property, т.к. помимо property дергается `__setattr__`
    def set_message(self, message: AttrDict):
        object.__setattr__(self, "_message", message)

    def __eq__(self, other: Event) -> bool:
        """
        Сравнение событий по их ID
        """
        return self.event_id == other.event_id

    def __str__(self):
        """
        Минималистичное отображение события
        """
        return f"Event(type={self.type!r})"

    def __getattr__(self, item):
        field = super().__getattr__(item)
        return AttrDict(field())
