from vkquick.ext.chatbot.filters.base import CommandFilter, Context
from vkquick.exceptions import FilterFailedError


class IgnoreBotsMessagesFilter(CommandFilter):
    def make_decision(self, ctx: Context) -> None:
        if ctx.mp.storage.from_id < 0:
            raise FilterFailedError()
