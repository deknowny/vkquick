import json

import attrdict
import pygments
import pygments.lexers
import pygments.formatters
import pygments.formatters.terminal
import pygments.token


class Event(attrdict.AttrMap):
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

    def __str__(self):
        data = json.dumps(self._mapping, indent=4, ensure_ascii=False)
        return pygments.highlight(
            data,
            pygments.lexers.JsonLexer(),
            pygments.formatters.TerminalFormatter(bg="light"),
        )

    # def get_text(self) -> str:
    #     """
    #     Возвращает текст сообщения вне зависимости от версии API или типа события
    #     Доступно только для событий `message_new` и `message_edit`
    #     """
    #     if self.type == "message_edit" or "message" not in self.object:
    #         return self.object.text
    #     else:
    #         return self.object.message.text
    #
    # # TODO

    def get_message_object(self):
        if "message" in self.object:
            return self.object.message
        else:
            return self.object
