from vkquick.tools import PEER
from .base import Validator


class DirectOnly(Validator):
    """
    Декоратор для валидации сообщения,
    которое должно быть отправленно только в лс
    """

    def validate(self, event) -> None:
        if event.object.message.peer_id >= PEER:
            raise ValueError("Message was sent in chat, not in direct")
