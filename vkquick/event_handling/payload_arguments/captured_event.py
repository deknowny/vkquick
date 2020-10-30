import typing as ty

import vkquick.base.payload_argument
import vkquick.events_generators.event
import vkquick.wrappers.user


class CapturedEvent(vkquick.base.payload_argument.PayloadArgument):
    async def init_value(
        self, event: vkquick.events_generators.event.Event
    ) -> ty.Any:
        return event
