from .base import Annotype

from attrdict import AttrMap


class Event(Annotype, AttrMap):
    """
    Событие LongPoll
    """

    @classmethod
    def prepare(cls, argname, event, func, bin_stack):
        return cls(event._mapping)

    def __str__(self):
        return f'<vkquick.annotypes.event.Event type="{self.type}">'

    __repr__ = __str__
