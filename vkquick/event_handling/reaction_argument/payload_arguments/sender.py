import typing as ty

import vkquick.event_handling.reaction_argument.payload_arguments.base
import vkquick.events_generators.event
import vkquick.wrappers.user


class Sender(
    vkquick.event_handling.reaction_argument.payload_arguments.base.PayloadArgument
):
    async def init_value(
        self, event: vkquick.events_generators.event.Event
    ) -> ty.Any:
        sender_id = event.get_message_object().from_id
        user = await vkquick.wrappers.user.User.build_from_id(sender_id)
        return user
