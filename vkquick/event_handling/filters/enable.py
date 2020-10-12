import dataclasses
import typing as ty


import vkquick.event_handling.filters.base
import vkquick.events_generators.event
import vkquick.event_handling.message
import vkquick.utils


@dataclasses.dataclass
class Enable(vkquick.event_handling.filters.base.Filter):

    enabled: bool = True

    async def make_decision(
        self, event: vkquick.events_generators.event.Event
    ) -> ty.Tuple[bool, str]:
        """
        Определяет, подходит ли событие по критериями фильтра
        """
        if self.enabled:
            decision = "Handling is enabled"
        else:
            decision = "Handling is disabled"
        return self.enabled, decision
