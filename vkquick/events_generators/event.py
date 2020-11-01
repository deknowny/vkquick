from __future__ import annotations
import json

import pygments.lexers
import pygments.formatters
from pygments import highlight
import pygments.formatters.terminal
import pygments.token

import vkquick.base.payload_argument
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

    def __new__(cls, mapping):
        if isinstance(mapping, list):
            elems = [vkquick.utils.AttrDict(i) for i in mapping]
            return super().__new__(cls, elems)
        else:
            return super().__new__(cls, mapping)

    def __init__(self, mapping):
        # User LongPoll:
        if isinstance(mapping, list):
            object.__setattr__(self, "type", mapping[0])
            object.__setattr__(self, "event_id", mapping[1])
        super().__init__(mapping)

    def get_message_object(self):
        """
        Возвращает объект сообщения в зависимости от версии
        API или же типа события
        """
        if isinstance(self(), list):
            # User LongPoll. Только для нового сообщения
            return vkquick.utils.AttrDict(
                {
                    "event_id": self[0],
                    "msg_id": self[1],
                    "flags": self[2],
                    "peer_id": self[3],
                    "timestamp": self[4],
                    "text": self[5],
                    "from_id": int(self[6]["from"])
                    if "from" in self[6]
                    else self[3],
                    "attachments": self[7],
                    "random_id": self[8],
                }
            )
        if "message" in self.object:
            return self.object.message
        elif isinstance(self(), dict):
            return self.object

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
        scheme = highlight(
            scheme,
            pygments.lexers.JsonLexer(),
            pygments.formatters.TerminalFormatter(bg="light"),
        )
        return scheme
