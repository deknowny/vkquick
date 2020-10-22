from __future__ import annotations
import json

import pygments.lexers
import pygments.formatters
from pygments import highlight, lexers, formatters
import pygments.formatters.terminal
import pygments.token

import vkquick.event_handling.reaction_argument.payload_arguments.base
import vkquick.utils


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


class Event(vkquick.utils.AttrDict):
    """
    Обертка для приходящего события в виде словаря.
    Позволяет обращаться к полям события как к атрибутам
    """

    def get_message_object(self):
        """
        Возвращает объект сообщения в зависимости от версии
        API или же типа события
        """
        if "message" in self.object:
            return self.object.message
        else:
            return self.object

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
        scheme = highlight(
            scheme,
            pygments.lexers.JsonLexer(),
            pygments.formatters.TerminalFormatter(bg="light"),
        )
        return scheme
