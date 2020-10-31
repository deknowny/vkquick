import typing as ty

import vkquick.base.filter
import vkquick.events_generators.event


class RetractAccessFor(vkquick.base.filter.Filter):

    passed_decision = "Пользователь не имеет ограничение к команде"
    not_passed_decision = "Пользователь имеет ограничение к команде"

    def __init__(self, *ids):
        self.ids = ids

    def make_decision(
        self, event: vkquick.events_generators.event.Event
    ) -> ty.Tuple[bool, str]:
        """
        Проверяет на доступ к команде
        """
        if event.get_message_object().from_id not in self.ids:
            return True, self.passed_decision
        return False, self.not_passed_decision
