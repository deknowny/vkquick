import typing as ty

import vkquick.base.payload_argument
import vkquick.events_generators.event
import vkquick.wrappers.user


class CapturedEvent(vkquick.base.payload_argument.PayloadArgument):
    """
    Событие, которое было получено
    """
    async def init_value(
        self, event: vkquick.events_generators.event.Event
    ) -> vkquick.events_generators.event.Event:
        return event
