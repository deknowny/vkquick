import abc


from vkquick.bases.filter import Filter
from vkquick.ext.chatbot.filters.command.context import CommandContext



class CommandFilter(Filter):

    @abc.abstractmethod
    def make_decision(self, ctx: CommandContext) -> None:
        ...