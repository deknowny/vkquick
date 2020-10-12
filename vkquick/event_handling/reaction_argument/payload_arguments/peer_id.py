import typing as ty

import vkquick.event_handling.reaction_argument.payload_arguments.base
import vkquick.events_generators.event


class PeerID(
    vkquick.event_handling.reaction_argument.payload_arguments.base.PayloadArgument
):
    async def init_value(
        self, event: vkquick.events_generators.event.Event
    ) -> int:
        return event.get_message_object().peer_id
