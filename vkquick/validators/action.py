from .base import Validator
from vkquick.annotypes import Annotype


class Action(Validator, Annotype):
    """
    Reaction to some message new actions
    """

    def __init__(self, *types):
        self.types = types

    @staticmethod
    def prepare(argname, event, func, bot, bin_stack):
        return event.object.message.action

    def isvalid(self, event, com, bot, bin_stack):
        if (
            "action" in event.object.message and
            event.object.message.action.type in self.types
        ):
            return (True, "")
        return (False, "No action or action.type is an another")
