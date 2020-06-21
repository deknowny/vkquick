from .base import Annotype


class Event(Annotype):
    @classmethod
    def prepare(cls, argname, event, func, bot, bin_stack):
        return cls.init(event)

    @classmethod
    def init(cls, event):
        self = object.__new__(cls)
        self.type = event.type
        self.object = event.object
        self.group_id = event.group_id

        return self

    def __str__(self):
        return f"<vq.Event type=\"{self.type}\">"

    __repr__ = __str__
