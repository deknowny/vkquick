from random import randint
from typing import Optional, List

from attrdict import AttrMap

from .uploader import Uploader
from vkquick import current
from vkquick.annotypes.base import Annotype


class Message(Annotype):
    """
    Используйте в своей реакции,
    чтобы отправить сообщение в диалог
    со всеми возможными параметрами ```messages.send```,
    откуда пришло событие, т.е. по умолчанию:

    `peer_id=event.object.message.peer_id`
    (если не был передан ни один из параметров
    `"user_id", "domain", "chat_id",
    "user_ids", "peer_ids"`)

    `random_id=random.randint(-2**31, +2**31)`


    ## Пример
    Классический hello world в ответ на пользовательскую команду ```hello``` или ```привет```

        import vkquick as vq


        @vq.Cmd(names=["hello", "привет"])
        @vq.Reaction("message_new")
        def hello_world():
            return vq.Message("Hello world!")

    Для ответов, содержащих только текст, вы можете просто вернуть текст

        import vkquick as vq


        @vq.Cmd(names=["hello", "привет"])
        @vq.Reaction("message_new")
        def hello_world():
            return "Hello, world!"
    """

    def __init__(
        self,
        message: Optional[int] = None,
        *,
        peer_id: Optional[int] = None,
        random_id: Optional[int] = None,
        user_id: Optional[int] = None,
        domain: Optional[str] = None,
        chat_id: Optional[int] = None,
        user_ids: Optional[List[int]] = None,
        peer_ids: Optional[List[int]] = None,
        lat: Optional[float] = None,
        long: Optional[float] = None,
        attachment: Optional[List[str]] = None,
        reply_to: Optional[int] = None,
        forward_messages: Optional[List[int]] = None,
        sticker_id: Optional[int] = None,
        group_id: Optional[int] = None,
        keyboard: Optional[str] = None,
        payload: Optional[str] = None,
        dont_parse_links: Optional[bool] = None,
        disable_mentions: Optional[bool] = None,
        intent: Optional[str] = None,
        expire_ttl: Optional[int] = None,
        silent: Optional[bool] = None,
        **kwargs,
    ):
        if random_id is None:
            random_id = randint(-2 * 31, 2 * 31)

        preload_data = locals().copy()
        del preload_data["self"]
        kwargs_vals = preload_data.pop("kwargs")
        preload_data.update(kwargs_vals)

        self._params = AttrMap(
            dict(filter(lambda x: x[1] is not None, preload_data.items()))
        )
        self._set_path()
        self._join_attach()

    def prepare(
        self,
        argname: str,
        event: "vkquick.annotypes.event.Event",
        func: "vkquick.reaction.Reaction",
        bin_stack: type,
    ):
        self._event = event
        return self

    async def __call__(self, *args, **kwargs):
        """
        Отправляет сообщение без `return`
        """
        self.__init__(*args, **kwargs)

        if self.params.peer_id is Ellipsis:
            self.params.peer_id = self._event.object.message.peer_id

        return await current.api.messages.send(**self.params)

    @property
    def params(self):
        """
        Возвращает параметры для ```messages.send```
        """
        return self._params

    def _join_attach(self):
        """
        Подготавливает вложения
        """
        if "attachment" in self._params:
            if isinstance(self._params.attachment, str):
                return

            if isinstance(self._params.attachment, list) or isinstance(
                self._params.attachment, tuple
            ):
                new_attachments = []
                for attach in self._params.attachment:
                    if isinstance(attach, Uploader):
                        new_attachments.append(repr(attach))
                    elif isinstance(attach, str):
                        new_attachments.append(attach)
                    else:
                        raise ValueError(
                            f"Invalid attachment type: {type(attach)}"
                        )
                self._params.attachment = ",".join(new_attachments)

    def _set_path(self):
        """
        Устанавливает peer_id в зависимости от того,
        были ли переданы другие параметры
        """
        if not (
            {"user_id", "domain", "chat_id", "user_ids", "peer_ids"}
            & set(self._params)
        ):
            self._params.peer_id = Ellipsis
