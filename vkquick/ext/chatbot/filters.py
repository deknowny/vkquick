import abc

from vkquick.bases.filter import Filter
from vkquick.exceptions import FilterFailedError
from vkquick.ext.chatbot.command.context import Context


class CommandFilter(Filter):
    @abc.abstractmethod
    def make_decision(self, ctx: Context) -> None:
        ...


class IgnoreBotsMessagesFilter(CommandFilter):
    def make_decision(self, ctx: Context) -> None:
        if ctx.mp.storage.from_id < 0:
            raise FilterFailedError()
