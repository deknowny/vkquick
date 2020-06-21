from .base import Annotype


class ClientInfo:
    """
    Info about user functionality
    """
    @classmethod
    def prepare(cls, argname, event, func, bot, bin_stack):
        return event.object.client_info
