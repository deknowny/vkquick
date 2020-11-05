from __future__ import annotations
import json
import functools
import typing as ty

import pygments
import pygments.lexers
import pygments.formatters
import pygments.formatters.terminal
import pygments.token

from vkquick.current import fetch
from vkquick.utils import AttrDict


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


class Event(AttrDict):
    """
    Обертка для приходящего события в виде словаря.
    Позволяет обращаться к полям события как к атрибутам
    """

    api = fetch("api_event", "api")

    @functools.cached_property
    def from_group(self):
        if isinstance(self(), list):
            return False
        return True

    @functools.cached_property
    def type(self) -> ty.Union[str, int]:
        if isinstance(self(), list):
            return self[0]
        return self["type"]

    @functools.cached_property
    def event_id(self) -> ty.Union[str, int]:
        if isinstance(self(), list):
            return self[1]
        return self["event_id"]

    def __eq__(self, other: Event) -> bool:
        """
        Сравнение событий по их айди
        """
        return self.event_id == other.event_id

    def __str__(self):
        """
        Минималистичное отображение события
        """
        return f"Event(type={self.type})"

    def pretty_view(self) -> str:
        """
        Цветное отображение JSON события вместе с индентами
        """
        scheme = json.dumps(self(), ensure_ascii=False, indent=4)
        scheme = pygments.highlight(
            scheme,
            pygments.lexers.JsonLexer(),
            pygments.formatters.TerminalFormatter(bg="light"),
        )
        return scheme
