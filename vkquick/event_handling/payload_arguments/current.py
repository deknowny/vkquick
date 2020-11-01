import typing as ty

import vkquick.base.payload_argument
import vkquick.events_generators.event
import vkquick.current


class Current(vkquick.base.payload_argument.PayloadArgument):
    """
    Возвращает объект из current по его имени
    """
    def __init__(self, current_object_name):
        self.current_object_name = current_object_name

    def init_value(
        self, event: vkquick.events_generators.event.Event
    ) -> ty.Any:
        return vkquick.current.curs[self.current_object_name]
