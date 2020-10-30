import typing as ty

import vkquick.base.payload_argument
import vkquick.events_generators.event
import vkquick.wrappers.user


class RepliedUser(vkquick.base.payload_argument.PayloadArgument):
    async def init_value(
        self, event: vkquick.events_generators.event.Event
    ) -> ty.Any:
        message = event.get_message_object()
        if "reply_message" in message:
            replied_user_id = message.reply_message.from_id
            replied_user = await vkquick.wrappers.user.User.build_from_id(
                replied_user_id
            )
            return replied_user
        return None
