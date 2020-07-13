from vkquick.tools import PEER

from .base import Annotype


class ChatID(Annotype):
    """
    Возаращет chat_id в соответствии типом беседа/диалог
    """

    def prepare(self, argname, event, func, bin_stack) -> int:
        if event.object.message.peer_id > PEER:
            return event.object.message.peer_id - PEER
        return event.object.message.peer_id
