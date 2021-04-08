from vkquick.ext.chatbot.filters.base import CommandFilter, CommandContext
from vkquick.exceptions import FilterFailedError


class IgnoreBotsMessagesFilter(CommandFilter):
    def make_decision(self, ctx: CommandContext) -> None:
        if ctx.mp.storage.from_id < 0:
            raise FilterFailedError()
