import vkquick.base.payload_argument
import vkquick.events_generators.event
import vkquick.wrappers.user
import vkquick.base.user_type


class Sender(vkquick.base.user_type.UserType):
    """
    Пользователь, отправивший сообщение
    """

    async def init_value(
        self, event: vkquick.events_generators.event.Event
    ) -> vkquick.wrappers.user.User:
        sender_id = event.get_message_object().from_id
        user = await vkquick.wrappers.user.User.build_from_id(
            sender_id, fields=self.fields, name_case=self.name_case
        )
        return user
