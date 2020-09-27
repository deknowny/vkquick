from __future__ import annotations
import attrdict

import vkquick.event_handling.reaction_argument.payload_arguments.base


class Event(
    attrdict.AttrMap,
    vkquick.event_handling.reaction_argument.payload_arguments.base.PayloadArgument,
):
    """
    Обертка для приходящего события в виде словаря.
    Позволяет обращаться к полям события как к атрибутам
    """

    def __repr__(self) -> str:
        return f"Event({self._mapping})"

    @staticmethod
    def init_value(event: Event):
        return event

    def get_message_object(self):
        if "message" in self.object:
            return self.object.message
        else:
            return self.object
