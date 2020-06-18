from .base import Annotype


class Event(Annotype):
    @staticmethod
    def prepare(argname, event, func, bot, bin_stack):
        return event
