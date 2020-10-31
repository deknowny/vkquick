import typing as ty

import vkquick.base
import vkquick.current
import vkquick.event_handling.message
import vkquick.events_generators
import vkquick.events_generators.event
import vkquick.base.payload_argument
import vkquick.utils


class Answer(vkquick.base.payload_argument.PayloadArgument):
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
    """

    api = vkquick.current.fetch("api_message", "api")

    def __init__(self):
        self.params = {}

    async def __call__(
        self,
        message: ty.Optional[str] = None,
        /,
        *,
        peer_id: ty.Optional[int] = None,
        random_id: ty.Optional[int] = None,
        user_id: ty.Optional[int] = None,
        domain: ty.Optional[str] = None,
        chat_id: ty.Optional[int] = None,
        user_ids: ty.Optional[ty.List[int]] = None,
        peer_ids: ty.Optional[ty.List[int]] = None,
        lat: ty.Optional[float] = None,
        long: ty.Optional[float] = None,
        attachment: ty.Optional[ty.List[str]] = None,
        reply_to: ty.Optional[int] = None,
        forward_messages: ty.Optional[ty.List[int]] = None,
        sticker_id: ty.Optional[int] = None,
        group_id: ty.Optional[int] = None,
        keyboard: ty.Optional[str] = None,
        payload: ty.Optional[str] = None,
        dont_parse_links: ty.Optional[bool] = None,
        disable_mentions: ty.Optional[bool] = None,
        intent: ty.Optional[str] = None,
        expire_ttl: ty.Optional[int] = None,
        silent: ty.Optional[bool] = None,
        subscribe_id: ty.Optional[int] = None,
        content_source: ty.Optional[str] = None,
        **kwargs,
    ):
        if random_id is None:
            random_id = vkquick.utils.random_id()
        breakpoint()
        for name, value in locals().items():
            if name == "kwargs":
                self.params.update(value)
            elif name != "self" and value is not None:
                self.params.update({name: value})

        await self.api.method("messages.send", self.params)

    async def init_value(
        self, event: ty.Optional[vkquick.events_generators.event.Event]
    ):
        breakpoint()
        self.params["peer_id"] = event.get_message_object().peer_id
        return self
