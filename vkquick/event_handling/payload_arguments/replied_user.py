import typing as ty

import vkquick.base.payload_argument
import vkquick.events_generators.event
import vkquick.wrappers.user
import vkquick.base.user_type


class RepliedUser(vkquick.base.user_type.UserType):
    """
    Пользователь из сообщения, на которое ответили. Если такого
    нет, значит будет `None`
    """

    async def init_value(
        self, event: vkquick.events_generators.event.Event
    ) -> ty.Any:
        message = event.get_message_object()
        if "reply_message" in message:
            replied_user_id = message.reply_message.from_id
            replied_user = await vkquick.wrappers.user.User.build_from_id(
                replied_user_id, fields=self.fields, name_case=self.name_case
            )
            return replied_user
        return None
