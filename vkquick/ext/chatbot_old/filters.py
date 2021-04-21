import abc

from vkquick.bases.filter import Filter
from vkquick.exceptions import FilterFailedError
from vkquick.ext.chatbot.command.context import Context


class CommandFilter(Filter):

    accepted_event_types = {"message_new", "message_reply", 4}

    @abc.abstractmethod
    async def make_decision(self, ctx: Context) -> None:
        ...


class IgnoreBotsMessagesFilter(CommandFilter):
    async def make_decision(self, ctx: Context) -> None:
        if ctx.msg.from_id < 0:
            raise FilterFailedError()
