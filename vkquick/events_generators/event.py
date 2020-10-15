from __future__ import annotations

import vkquick.event_handling.reaction_argument.payload_arguments.base
import vkquick.utils


class Event(
    vkquick.utils.AttrDict,
    vkquick.event_handling.reaction_argument.payload_arguments.base.PayloadArgument,
):
    """
    Обертка для приходящего события в виде словаря.
    Позволяет обращаться к полям события как к атрибутам
    """

    @staticmethod
    def init_value(event: Event):
        return event

    def get_message_object(self):
        if "message" in self.object:
            return self.object.message
        else:
            return self.object

    def __str__(self):
        return f"Event(type={self.type})"
