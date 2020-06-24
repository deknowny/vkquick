from .base import Annotype

from attrdict import AttrMap


class Event(Annotype, AttrMap):
    """
    Событие LongPoll
    """
    @classmethod
    def prepare(cls, argname, event, func, bot, bin_stack):
        return cls.__new__(cls, event._mapping)

    def __str__(self):
        return f"<vq.Event type=\"{self.type}\">"

    __repr__ = __str__
