from .base import Annotype


class PeerID(Annotype):
    """
    Возаращет peer_id диалога/беседы, откуда пришло сообщение
    """

    def prepare(self, argname, event, func, bin_stack) -> int:
        return event.object.message.peer_id
