import enum

import vkquick.base.filter
import vkquick.events_generators.event


class ChatOnlyStatus(vkquick.base.filter.DecisionStatus):
    PASSED = enum.auto()
    NOT_PASSED = enum.auto()


class ChatOnly(vkquick.base.filter.Filter):

    passed_decision = vkquick.base.filter.Decision(True, "Сообщение отправлено в чат")
    not_passed_decision = vkquick.base.filter.Decision(False, "Сообщение отправлено в личные сообщения")
    passed_response = vkquick.base.filter.FilterResponse(ChatOnlyStatus.PASSED, passed_decision)
    not_passed_response = vkquick.base.filter.FilterResponse(ChatOnlyStatus.NOT_PASSED, not_passed_decision)

    def make_decision(
        self, event: vkquick.events_generators.event.Event
    ) -> vkquick.base.filter.FilterResponse:
        """
        Определяет откуда отправлено сообщение
        """
        if event.get_message_object().peer_id > vkquick.peer(0):
            return self.passed_response
        return self.not_passed_response
