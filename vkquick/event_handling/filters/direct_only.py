"""
DirectOnly фильтр
"""
import enum

import vkquick.base.filter
import vkquick.events_generators.event


class DirectOnlyStatus(vkquick.base.filter.DecisionStatus):
    PASSED = enum.auto()
    NOT_PASSED = enum.auto()


class DirectOnly(vkquick.base.filter.Filter):
    """
    Делает команду доступной только в лс
    """

    passed_decision = vkquick.base.filter.Decision(
        True, "Сообщение отправлено в личные сообщения"
    )
    not_passed_decision = vkquick.base.filter.Decision(
        False, "Сообщение отправлено в лс"
    )
    passed_response = vkquick.base.filter.FilterResponse(
        DirectOnlyStatus.PASSED, passed_decision
    )
    not_passed_response = vkquick.base.filter.FilterResponse(
        DirectOnlyStatus.NOT_PASSED, not_passed_decision
    )

    def make_decision(
        self, event: vkquick.events_generators.event.Event
    ) -> vkquick.base.filter.FilterResponse:
        if event.get_message_object().peer_id < vkquick.peer():
            return self.passed_response
        return self.not_passed_response
