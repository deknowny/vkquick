import vkquick.event_handling.payload_arguments.message
import vkquick.events_generators.event
import vkquick.base.payload_argument


class Answer(
    vkquick.event_handling.payload_arguments.message.Message,
    vkquick.base.payload_argument.PayloadArgument,
):
    """
    Используйте в своей реакции,
    чтобы отправить сообщение в диалог
    со всеми возможными параметрами `messages.send`,
    откуда пришло событие, т.е. по умолчанию:

    `peer_id=event.object.message.peer_id`
    (если не был передан ни один из параметров
    `"user_id", "domain", "chat_id",
    "user_ids", "peer_ids"`)

    `random_id=random.randint(-2**31, +2**31)`
    """

    def __init__(self):
        self.params = {}

    def init_value(self, event: vkquick.events_generators.event.Event):
        self.params["peer_id"] = event.get_message_object().peer_id
        return self

    __call__ = (
        vkquick.event_handling.payload_arguments.message.Message.__init__
    )
