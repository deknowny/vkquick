import abc


from vkquick.bases.filter import Filter
from vkquick.ext.chatbot.filters.command.context import Context


class CommandFilter(Filter):
    @abc.abstractmethod
    def make_decision(self, ctx: Context) -> None:
        ...
