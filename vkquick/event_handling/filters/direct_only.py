import dataclasses
import typing as ty


import vkquick.event_handling.filters.base
import vkquick.events_generators.event
import vkquick.event_handling.message
import vkquick.utils


@dataclasses.dataclass
class DirectOnly(vkquick.event_handling.filters.base.Filter):

    async def make_decision(
        self, event: vkquick.events_generators.event.Event
    ) -> ty.Tuple[bool, str]:
        """
        Определяет откуда приходит сообщение
        """

        if event.get_message_object().peer_id < 2e9:
            return True, "Сообщение пришло с личных сообщений"
        return False, "Сообщение пришло с чата"
