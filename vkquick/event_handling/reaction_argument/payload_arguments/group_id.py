import typing as ty

import vkquick.event_handling.reaction_argument.payload_arguments.base
import vkquick.events_generators.event


class GroupID(
    vkquick.event_handling.reaction_argument.payload_arguments.base.PayloadArgument
):
    async def init_value(
        self, event: vkquick.events_generators.event.Event
    ) -> int:
        return event.group_id
