from typing import Optional
from json import dumps

from .base import Annotype
from vkquick import current


class CallbackAnswer(Annotype):
    """
    Упрощает работу с методом `messages.sendMessageEventAnswer`
    """

    params: dict

    def prepare(
        self,
        argname: str,
        event: "vkquick.annotypes.event.Event",
        func: "vkquick.reaction.Reaction",
        bin_stack: type,
    ):
        self.params = dict(
            event_id=event.object.event_id,
            user_id=event.object.user_id,
            peer_id=event.object.peer_id,
            conversation_message_id=event.object.conversation_message_id,
        )
        return self

    def show_snackbar(self, text: str):
        """
        Показывает исчезающее сообщение
        """
        self._prepare_event_data("show_snackbar", {"text": text})
        return self

    def open_link(self, link: str):
        """
        Открывает ссылку
        """
        self._prepare_event_data("open_link", {"link": link})
        return self

    def open_app(self, *, app_id: int, owner_id: Optional[int], hash_: str):
        """
        Открывает Mini Apps
        """
        self._prepare_event_data(
            "open_app", dict(app_id=app_id, owner_id=owner_id, hash=hash_)
        )
        return self

    def __await__(self):
        """
        Сделайте await, чтобы отправить запрос
        """
        return self._make_request().__await__()

    def _prepare_event_data(self, type_, data):
        data.update(type=type_)
        self.params.update(event_data=dumps(data, ensure_ascii=False))

    async def _make_request(self):
        await current.api.messages.send_message_event_answer(**self.params)
