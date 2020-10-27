import typing as ty


import vkquick.event_handling.filters.base
import vkquick.events_generators.event
import vkquick.utils


class Enable(vkquick.event_handling.filters.base.Filter):

    passed_decision = "Обработка событий включена"
    not_passed_decision = "Обработка событий отключена"

    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def make_decision(
        self, event: vkquick.events_generators.event.Event
    ) -> ty.Tuple[bool, str]:
        """
        Определяет, подходит ли событие по критериям фильтра
        """
        if self.enabled:
            decision = self.passed_decision
        else:
            decision = self.not_passed_decision
        return self.enabled, decision
