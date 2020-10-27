import typing as ty

import vkquick.event_handling.payload_arguments.base
import vkquick.events_generators.event
import vkquick.current


class Current(vkquick.event_handling.payload_arguments.base.PayloadArgument):
    def __init__(self, current_object_name):
        self.current_object_name = current_object_name

    def init_value(
        self, event: vkquick.events_generators.event.Event
    ) -> ty.Any:
        return vkquick.current.objects[self.current_object_name]
