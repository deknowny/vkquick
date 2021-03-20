from __future__ import annotations

from vkquick.api import API
from vkquick.event_handler.context import EventHandlingContext
from vkquick.chatbot_extension.wrappers.message import Message


class CommandContext:
    def __init__(
        self, *, ehctx: EventHandlingContext, message: Message
    ) -> None:
        self._ehctx = ehctx
        self._message = message
        self._command_validating_status = None
        self._command_validating_payload = None


    @property
    def command_validating_status(self):
        return self._command_validating_status

    @command_validating_status.setter
    def command_validating_status(self, value):
        pass

    @property
    def api(self) -> API:
        return self._ehctx.api

    @property
    def ehctx(self) -> EventHandlingContext:
        return self._ehctx

    @property
    def msg(self) -> Message:
        return self._message
