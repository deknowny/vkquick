from vkquick.tools import PEER
from .base import Validator


class DirectOnly(Validator):
    """
    Декоратор для валидации сообщения,
    которое должно быть отправленно только в лс
    """

    def isvalid(self, event, com, bin_stack):
        if event.object.message.peer_id < PEER:
            return (True, "")
        return (False, "Message was sent in chat, not in direct")
