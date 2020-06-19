from .base import Annotype


class Event(Annotype):
    @classmethod
    def prepare(cls, argname, event, func, bot, bin_stack):
        return event
